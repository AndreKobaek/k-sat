/*****************************************************************************************[Main.cc]
abcdSAT r17 -- Copyright (c) 2017, Jingchao Chen  Donghua University   

abcdSAT r17 sources are obtained by modifying Glucose (see below Glucose copyrights) and abcdSAT drup. 
Permissions and copyrights of
abcdSAT r17 are exactly the same as Glucose.

--------------------------------------------------------
 Glucose -- Copyright (c) 2009, Gilles Audemard, Laurent Simon
				CRIL - Univ. Artois, France
				LRI  - Univ. Paris Sud, France
 
Glucose sources are based on MiniSat (see below MiniSat copyrights). Permissions and copyrights of
Glucose are exactly the same as Minisat on which it is based on. (see below).

---------------

Copyright (c) 2003-2006, Niklas Een, Niklas Sorensson
Copyright (c) 2007-2010, Niklas Sorensson

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT
OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
**************************************************************************************************/

#include <errno.h>

#include <signal.h>
#include <zlib.h>
#include <sys/resource.h>

#include "utils/System.h"
#include "utils/ParseUtils.h"
#include "utils/Options.h"
#include "core/Dimacs.h"
#include "simp/SimpSolver.h"

char* input_file = NULL;

using namespace abcdSAT;

//=================================================================================================


void printStats(Solver *solver)
{
    double cpu_time = cpuTime();
    double mem_used = 0;
    printf("c restarts              : %" PRIu64" (%" PRIu64" conflicts in avg)\n", solver->starts,(solver->starts>0 ?solver->conflicts/solver->starts : 0));
    printf("c blocked restarts      : %" PRIu64" \n", solver->nbstopsrestarts);
    printf("c nb ReduceDB           : %ld\n", (long int)solver->nbReduceDB);
    printf("c nb removed Clauses    : %ld\n",(long int)solver->nbRemovedClauses);
    printf("c nb learnts DL2        : %ld\n", (long int)solver->nbDL2);
    printf("c nb learnts size 2     : %ld\n", (long int)solver->nbBin);
    printf("c nb learnts size 1     : %ld\n", (long int)solver->nbUn);

    printf("c conflicts             : %-12" PRIu64"   (%.0f /sec)\n", solver->conflicts   , solver->conflicts/cpu_time);
    printf("c decisions             : %-12" PRIu64"   (%4.2f %% random) (%.0f /sec)\n", solver->decisions, (float)solver->rnd_decisions*100 / (float)solver->decisions, solver->decisions   /cpu_time);
    printf("c propagations          : %-12" PRIu64"   (%.0f /sec)\n", solver->propagations, solver->propagations/cpu_time);
    printf("c conflict literals     : %-12" PRIu64"   (%4.2f %% deleted)\n", solver->tot_literals, (solver->max_literals - solver->tot_literals)*100 / (double)solver->max_literals);
    printf("c nb reduced Clauses    : %ld\n", (long int)solver->nbReducedClauses);
    
    if (mem_used != 0) printf("Memory used           : %.2f MB\n", mem_used);
    printf("c CPU time              : %g s\n", cpu_time);
}

static Solver* solver;
static void SIGINT_exit(int signum) {
    printf("\n"); printf("c *** INTERRUPTED signum=%d ***\n",signum);
    if (solver->verbosity > 0){
        printStats(solver);
        printf("\n"); printf("c *** INTERRUPTED ***\n"); }
    _exit(1); 
}

void verifyModel(char* filename, vec<bool> & true_var)
{
    SimpSolver  S;
    gzFile in = gzopen(filename, "rb");
        if (in == NULL)
            printf("ERROR! Could not open file: %s\n", filename), exit(1);
           
// Parse CNF:
   printf("c final verify filename=%s \n",filename);
  
    parse_DIMACS(in, S);
    gzclose(in);
  
// Check satisfaction:
   vec<CRef>& cs = S.clauses;
  
   for (int i = 0; i < cs.size(); i++){
         Clause& c = S.ca[cs[i]];
        for (int j = 0; j < c.size(); j++){
              if (sign(c[j])==1 && true_var[var(c[j])]==false ) goto Satisfied;
              if (sign(c[j])==0 && true_var[var(c[j])]==true ) goto Satisfied;
        }
        printf("s INDETERMINATE\n");
        printf("c FALSE MODEL!!!\n");
        printf("c {");
        for (int j = 0; j < c.size(); j++){
               if(sign(c[j])) printf("-");
               printf("%d:%d ", var(c[j])+1, true_var[var(c[j])]);
        }
        printf(" }\n");
        exit(0);

      Satisfied:;
    }
}
float * size_diff;
void init_weight()
{
	int i, longest_clause = 100; 
	size_diff = (float *) malloc(sizeof(float) * longest_clause );
	size_diff[0]=size_diff[1] = 0.0;
	for( i = 2; i < longest_clause; i++ )  size_diff[ i ] = (float)pow(5.0, 2.0-i);
}

static const char* _certified = "CORE -- CERTIFIED UNSAT";

FILE*  certifiedOutput;
bool   certifiedUNSAT;   // tarce back UNSAT proof
void   init_rand_seed ();
   
//=================================================================================================
// Main:

int main(int argc, char** argv)
{
      init_weight();
      init_rand_seed ();
 
      try {
        printf("c\nc This is abcdSAT_r17 by Jingchao Chen, May 31,2017\n");
        
#if defined(__linux__)
        fpu_control_t oldcw, newcw;
        _FPU_GETCW(oldcw); newcw = (oldcw & ~_FPU_EXTENDED) | _FPU_DOUBLE; _FPU_SETCW(newcw);
#endif
        // Extra options:
        //
        IntOption    verb   ("MAIN", "verb",   "Verbosity level (0=silent, 1=some, 2=more).", 0, IntRange(0, 2));
        IntOption    vv  ("MAIN", "vv",   "Verbosity every vv conflicts", 10000, IntRange(1,INT32_MAX));
        BoolOption   pre    ("MAIN", "pre",    "Completely turn on/off any preprocessing.", true);
        StringOption dimacs ("MAIN", "dimacs", "If given, stop after preprocessing and write the result to this file.");
        IntOption    cpu_lim("MAIN", "cpu-lim","Limit on CPU time allowed in seconds.\n", INT32_MAX, IntRange(0, INT32_MAX));
        IntOption    mem_lim("MAIN", "mem-lim","Limit on memory usage in megabytes.\n", INT32_MAX, IntRange(0, INT32_MAX));
        BoolOption    opt_certified      (_certified, "certified",    "Certified UNSAT using DRUP format", false);
        StringOption  opt_certified_file      (_certified, "certified-output",    "Certified UNSAT output file", "NULL");
 
        parseOptions(argc, argv, true);
        
        SimpSolver  *S=  new SimpSolver();

        certifiedUNSAT = opt_certified;
        if(certifiedUNSAT) {
            if(!strcmp(opt_certified_file,"NULL")) {
                   certifiedOutput = stdout;
            } else {
              //   certifiedOutput =  fopen(opt_certified_file, "wb");
                 certifiedOutput =  fopen64(opt_certified_file, "wb");	    
            }
        }

        double      initial_time = cpuTime();

        if (!pre) S->eliminate(true);

        S->verbosity = verb;
        S->verbEveryConflicts = vv;
        solver = S;
        // Use signal handlers that forcibly quit until the solver will be able to respond to
        // interrupts:
        signal(SIGINT, SIGINT_exit);
        signal(SIGXCPU,SIGINT_exit);

        // Set limit on CPU-time:
        if (cpu_lim != INT32_MAX){
            rlimit rl;
            getrlimit(RLIMIT_CPU, &rl);
            if (rl.rlim_max == RLIM_INFINITY || (rlim_t)cpu_lim < rl.rlim_max){
                rl.rlim_cur = cpu_lim;
                if (setrlimit(RLIMIT_CPU, &rl) == -1)
                    printf("c WARNING! Could not set resource limit: CPU-time.\n");
            } }

        // Set limit on virtual memory:
        if (mem_lim != INT32_MAX){
            rlim_t new_mem_lim = (rlim_t)mem_lim * 1024*1024;
            rlimit rl;
            getrlimit(RLIMIT_AS, &rl);
            if (rl.rlim_max == RLIM_INFINITY || new_mem_lim < rl.rlim_max){
                rl.rlim_cur = new_mem_lim;
                if (setrlimit(RLIMIT_AS, &rl) == -1)
                    printf("c WARNING! Could not set resource limit: Virtual memory.\n");
            } }
        
        if (argc == 1)
            printf("c Reading from standard input... Use '--help' for help.\n");

        input_file=argv[1];
     
        gzFile in = (argc == 1) ? gzdopen(0, "rb") : gzopen(argv[1], "rb");
        if (in == NULL)
            printf("c ERROR! Could not open file: %s\n", argc == 1 ? "<stdin>" : argv[1]), exit(1);
    
       if (certifiedUNSAT) S->verbosity = 0;

       if (S->verbosity > 0){
            printf("c ========================================[ Problem Statistics ]===========================================\n");
            printf("c |                                                                                                       |\n"); 
        }
        
        parse_DIMACS(in, *S);
        gzclose(in);
       FILE* res = NULL;

       if (S->verbosity > 0){
            printf("c |  Number of variables:  %12d                                                                   |\n", S->nVars());
            printf("c |  Number of clauses:    %12d                                                                   |\n", S->nClauses()); }
        
        double parsed_time = cpuTime();
        if (S->verbosity > 0){
            printf("c |  Parse time:           %12.2f s                                                                 |\n", parsed_time - initial_time);
            printf("c |                                                                                                       |\n"); }

       double simplified_time;
       lbool ret;
       if(S->clauses.size()<=2000000 && S->nVars()<500000){
          SimpSolver  *newSolver=new SimpSolver();
          if(S->nVars()<1500) S->copyto(newSolver);
   
          ret= S->probe();
          if(ret != l_Undef) goto verify;
        
          if(S->nVars()>=1500) S->copyto(newSolver); // newSolver->Simp_equ = S->equhead;
          delete S;
          solver = S = newSolver;
       }
       S->eliminate(true);
       simplified_time = cpuTime();
       if (S->verbosity > 0){
            printf("c |  Simplification time:  %12.2f s                                                                 |\n", simplified_time - parsed_time);
            printf("c |                                                                                                       |\n"); }

        if (!S->okay()){
            if (res != NULL) fprintf(res, "UNSAT\n"), fclose(res);
            if (S->verbosity > 0){
 	        printf("c =========================================================================================================\n");
                printf("c Solved by simplification\n");
                printStats(S);
                printf("\n"); 
             }
             if (certifiedUNSAT) {
                   fprintf(certifiedOutput, "0\n");
                   fclose(certifiedOutput);
             }
             printf("s UNSATISFIABLE\n");
             printStats(S);
             return 20;
        }

        if (dimacs){
            if (S->verbosity > 0)
                printf("c =======================================[ Writing DIMACS ]===============================================\n");
            S->toDimacs((const char*)dimacs);
            if (S->verbosity > 0) printStats(S);
            exit(0);
        }

       {
         vec<Lit> dummy;
         ret = S->solveLimited(dummy);
       }
verify:
       if (certifiedUNSAT && ret == l_False) {
              fprintf(certifiedOutput, "0\n");
              printf("s UNSATISFIABLE\n");
              fclose(certifiedOutput);
              printStats(S);
              return 20;
       }
//#ifdef VERIFY_MODEL
        if (ret==l_True && input_file != NULL && S->nVars() < 50000){
           vec<bool>   VarValue(S->nVars(), false);
          for (int i = 0; i < S->nVars(); i++)
	      if (S->model[i] == l_True) VarValue[i]=true;
              else VarValue[i]=false;
          
            verifyModel(input_file, VarValue);
            printf("c OK! verified \n");
        }
//#endif
        
       // if (S->verbosity > 0){
            printStats(S);
            printf("\n"); 
       //}

      
        printf(ret == l_True ? "s SATISFIABLE\n" : ret == l_False ? "s UNSATISFIABLE\n" : "s INDETERMINATE\n");
	if(ret==l_True) {
	  printf("v ");
          int vars=S->nVars();
          if(S->originVars) vars=S->originVars;
          for (int i = 0; i < vars; i++)
	    if (S->model[i] != l_Undef)
	      printf("%s%s%d", (i==0)?"":" ", (S->model[i]==l_True)?"":"-", i+1);
	  printf(" 0\n");
 	}
        if (res != NULL){
            if (ret == l_True){
                fprintf(res, "SAT\n");
                for (int i = 0; i < S->nVars(); i++)
                    if (S->model[i] != l_Undef)
                        fprintf(res, "%s%s%d", (i==0)?"":" ", (S->model[i]==l_True)?"":"-", i+1);
                fprintf(res, " 0\n");
            }else if (ret == l_False)
                fprintf(res, "UNSAT\n");
            else
                fprintf(res, "INDET\n");
            fclose(res);
        }

#ifdef NDEBUG
        exit(ret == l_True ? 10 : ret == l_False ? 20 : 0);     // (faster than "return", which will invoke the destructor for 'Solver')
#else
        return (ret == l_True ? 10 : ret == l_False ? 20 : 0);
#endif
    } catch (OutOfMemoryException&){
	        printf("c =========================================================================================================\n");
        printf("INDETERMINATE\n");
        exit(0);
    }
}

