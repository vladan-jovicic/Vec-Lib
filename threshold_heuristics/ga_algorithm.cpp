# include <cstdlib>
# include <iostream>
# include <iomanip>
# include <fstream>
# include <iomanip>
# include <cmath>
# include <ctime>
# include <cstring>
# include <vector>
# include <sstream>

using namespace std;
// 
//  Change any of these parameters to match your needs 
//
# define POPSIZE 100
# define MAXGENS 1000
# define NVARS 4
# define PXOVER 0.4
# define PMUTATION 0.3
//
//  Each GENOTYPE is a member of the population, with
//  gene: a string of variables,
//  fitness: the fitness
//  upper: the variable upper bounds,
//  lower: the variable lower bounds,
//  rfitness: the relative fitness,
//  cfitness: the cumulative fitness.
//


struct point {
  int x; int y;
};

vector< vector<point> > data;


vector< double > eval;
//vector< double > nbRealCurves;
//vector< double > nbNoises; 
//vector< vector<double> > brutRepli;
vector< double > meanDist1; 
vector< double > meanDist2; 
vector< double > meanNbPoints; 
vector< double > nbCurves;

struct genotype
{
  double gene[NVARS]; // var 0 = lowerBound, var 1 = upperBound, var 3 = coeff sur les nbrBonnes, var 4 = coeff sur les pas bonnes
  double fitness;
  double upper[NVARS];
  double lower[NVARS];
  double rfitness;
  double cfitness;
  int K;
};

struct genotype population[POPSIZE+1];
struct genotype newpopulation[POPSIZE+1]; 

int main (int argc, char* argv[]);
void crossover ( int &seed );
void elitist ( );
void evaluate ( );
int i4_uniform_ab ( int a, int b, int &seed );
void initialize ( string filename, int &seed );
void keep_the_best ( );
void mutate ( int &seed );
double r8_uniform_ab ( double a, double b, int &seed );
void report ( int generation );
void selector ( int &seed );
void timestamp ( );
void Xover ( int one, int two, int &seed );


void read_file (string filename) {

  ifstream infile (filename, fstream::binary);
  
  if (!infile) {
    cout << "wrong filename";
    return;
  }

  int K = 0, c = 0;
  string line;
  while( getline(infile, line) ) {
    //cout << line << endl;
    if (line[0] == '#') {
      vector<point> temp;
      data.push_back(temp);
    }
    else if (line[0] != 'E') {
      istringstream iss (line);
      int a, b;
      char c; 
      point p;
      iss >> a >> c >> b; 
      p.x = a; p.y = b;
      //cout << p.x << c << p.y << "  ;  ";
      data[data.size()-1].push_back(p);
    }

    else { // end of K;
      nbCurves.push_back(0);
      meanNbPoints.push_back(0);
      meanDist1.push_back(0);
      meanDist2.push_back(0);
      vector< double> t_meanDist1 (data.size(), 0); 
      vector< double> t_meanDist2 (data.size(), 0); 
      vector< double> t_meanNbPoints (data.size(), 0); 
      
      for (int c = 0; c < data.size(); c++) {
        //cerr << "c = " << c << endl;
        point firstP = data[c][0];
        point lastP = data[c][0];
        for (int p = 1; p < data[c].size(); p++) {
          t_meanDist1[c] += abs(data[c][p].x - lastP.x) + abs(data[c][p].y - lastP.y);
          t_meanDist2[c] += sqrt(pow(data[c][p].x - lastP.x,2) + pow(data[c][p].y - lastP.y, 2) );
          lastP = data[c][p];
        }
        t_meanDist1[c] += abs(firstP.x - lastP.x) + abs(firstP.y - lastP.y);
        t_meanDist2[c] += pow(firstP.x - lastP.x,2) + pow(firstP.y - lastP.y, 2);

        t_meanNbPoints[c] += data[c].size();
        t_meanDist2[c] /= data[c].size();
        t_meanDist1[c] /= data[c].size();
      }
      for (int c = 0; c < data.size(); c++) {
        meanNbPoints[K] += t_meanNbPoints[c];
        meanDist1[K] += t_meanDist1[c];
        meanDist2[K] += t_meanDist2[c];
      }
      nbCurves[K] = data.size();
      meanNbPoints[K] /= nbCurves[K];
      meanDist1[K] /= nbCurves[K];
      meanDist2[K] /= nbCurves[K];
      /*cout << endl << endl << endl;
      cout << nbCurves[K] << " " <<
      meanNbPoints[K] <<" " <<
      meanDist1[K] << " " <<
      meanDist2[K] << endl;
       */
      data.clear();
      K++;
      cout << K << " done" << endl;

    }
  }
  
  double maxNbPoints (0), maxNbCurves (0), maxMeanD1 (0), maxMeanD2 (0);
  for (int k = 0; k < nbCurves.size(); k++) {
    maxNbPoints = max(maxNbPoints, meanNbPoints[k]);
    maxNbCurves = max(maxNbCurves, nbCurves[k]);
    maxMeanD1 = max(maxMeanD1, meanDist1[k]);
    maxMeanD2 = max(maxMeanD2, meanDist2[k]);
  }
  for (int k = 0; k < nbCurves.size(); k++) {
    meanNbPoints[k] /= maxNbPoints;
    nbCurves[k] /= maxNbCurves;
    meanDist1[k] /= maxMeanD1;
    meanDist2[k] /= maxMeanD2;
  }
}

/*
void create_indicators(double lowerBound, double upperBound) {
  nbNoises.clear();
  nbRealCurves.clear();

  for (int K = 0; K < data.size(); K++) {
    nbNoises.push_back(0);
    nbRealCurves.push_back(0);

    int size_c = data[K].size();
    double maxi = 0;
    vector< double> scores;
    for (int c = 0; c < size_c; c++) {
      if (data[K][c].size() > 1) {
        double score;
        point lastPoint = data[K][c][0];
        for (int p = 1; p < data[K][c].size(); p++) {
          score += sqrt(pow(data[K][c][p].x - lastPoint.x,2) + pow(data[K][c][p].y - lastPoint.y, 2) );
          lastPoint = data[K][c][p];
        }
        score /= data[K][c].size();

        scores.push_back(score);
        
        if (score > maxi)
          maxi = score;
      }
      else
        scores.push_back(0);
    }

    for (int c = 0; c < size_c; c++) {
      scores[c] /= maxi;
      if (scores[c] < lowerBound)
        nbNoises[K]++;
      if (scores[c] > upperBound)
        nbRealCurves[K]++;
    }
  }
}*/



//****************************************************************************80

int main (int argc, char* argv[])
//****************************************************************************80
//
//  Purpose:
//
//    MAIN supervises the genetic algorithm.
//
//  Discussion:
//
//    Each generation involves selecting the best 
//    members, performing crossover & mutation and then 
//    evaluating the resulting population, until the terminating 
//    condition is satisfied   
//
//    This is a simple genetic algorithm implementation where the 
//    evaluation function takes positive values only and the 
//    fitness of an individual is the same as the value of the 
//    objective function.  
//
//  Licensing:
//
//    This code is distributed under the GNU LGPL license. 
//
//  Modified:
//
//    28 April 2014
//
//  Author:
//
//    Original version by Dennis Cormier and Sita Raghavan.
//    This C++ version by John Burkardt.
//
//  Reference:
//
//    Zbigniew Michalewicz,
//    Genetic Algorithms + Data Structures = Evolution Programs,
//    Third Edition,
//    Springer, 1996,
//    ISBN: 3-540-60676-9,
//    LC: QA76.618.M53.
//
//  Parameters:
//
//    MAXGENS is the maximum number of generations.
//
//    NVARS is the number of problem variables.
//
//    PMUTATION is the probability of mutation.
//
//    POPSIZE is the population size. 
//
//    PXOVER is the probability of crossover.                          
//
{
  string filename = "ga_input.txt";
  string dataToAnalyse = argv[1];

  int generation;
  int i;
  int seed;

  timestamp ( );
  
  
  cout << "\n";
  cout << "SIMPLE_GA:\n";
  cout << "  C++ version\n";
  cout << "  A simple example of a genetic algorithm.\n";

  if ( NVARS < 2 )
  {
    cout << "\n";
    cout << "  The crossover modification will not be available,\n";
    cout << "  since it requires 2 <= NVARS.\n";
  }

  seed = 123456789;

  read_file(dataToAnalyse);

  //for (int k = 0; k < data.size(); k++) 
    //cerr << "K : " << k << " " << data[k].size() << endl;
  initialize ( filename, seed );

  evaluate ( );

  keep_the_best ( );

  for ( generation = 0; generation < MAXGENS; generation++ )
  {
    selector ( seed );
    crossover ( seed );
    mutate ( seed );
    report ( generation );
    evaluate ( );
    elitist ( );
  }

  cout << "\n";
  cout << "  Best member after " << MAXGENS << " generations:\n";
  cout << "\n";

  for ( i = 0; i < NVARS; i++ )
  {
    cout << "  var(" << i << ") = " << population[POPSIZE].gene[i] << "\n";
  }

  cout << "\n";
  cout << "  Best fitness = " << population[POPSIZE].fitness << "\n"
       << "  Best K       = " << population[POPSIZE].K << endl;
//
//  Terminate.
//
  cout << "\n";
  cout << "SIMPLE_GA:\n";
  cout << "  Normal end of execution.\n";
  cout << "\n";
  timestamp ( );

  return 0;
}
//****************************************************************************80

void crossover ( int &seed )

//****************************************************************************80
// 
//  Purpose:
//
//    CROSSOVER selects two parents for the single point crossover.
//
//  Licensing:
//
//    This code is distributed under the GNU LGPL license. 
//
//  Modified:
//
//    28 April 2014
//
//  Author:
//
//    Original version by Dennis Cormier and Sita Raghavan.
//    This C++ version by John Burkardt.
//
//  Local parameters:
//
//    Local, int FIRST, is a count of the number of members chosen.
//
//  Parameters:
//
//    Input/output, int &SEED, a seed for the random number generator.
//
{
  const double a = 0.0;
  const double b = 1.0;
  int mem;
  int one;
  int first = 0;
  double x;

  for ( mem = 0; mem < POPSIZE; ++mem )
  {
    x = r8_uniform_ab ( a, b, seed );

    if ( x < PXOVER )
    {
      ++first;

      if ( first % 2 == 0 )
      {
        Xover ( one, mem, seed );
      }
      else
      {
        one = mem;
      }

    }
  }
  return;
}
//****************************************************************************80

void elitist ( )

//****************************************************************************80
// 
//  Purpose:
//
//    ELITIST stores the best member of the previous generation.
//
//  Discussion:
//
//    The best member of the previous generation is stored as 
//    the last in the array. If the best member of the current 
//    generation is worse then the best member of the previous 
//    generation, the latter one would replace the worst member 
//    of the current population.
//
//  Licensing:
//
//    This code is distributed under the GNU LGPL license. 
//
//  Modified:
//
//    29 December 2007
//
//  Author:
//
//    Original version by Dennis Cormier and Sita Raghavan.
//    This C++ version by John Burkardt.
//
//  Local parameters:
//
//    Local, double BEST, the best fitness value.
//
//    Local, double WORST, the worst fitness value.
//
{
  int i;
  double best;
  int best_mem;
  double worst;
  int worst_mem;

  best = population[0].fitness;
  worst = population[0].fitness;

  for ( i = 0; i < POPSIZE - 1; ++i )
  {
    if ( population[i+1].fitness < population[i].fitness )
    {

      if ( best <= population[i].fitness )
      {
        best = population[i].fitness;
        best_mem = i;
      }

      if ( population[i+1].fitness <= worst )
      {
        worst = population[i+1].fitness;
        worst_mem = i + 1;
      }

    }
    else
    {

      if ( population[i].fitness <= worst )
      {
        worst = population[i].fitness;
        worst_mem = i;
      }

      if ( best <= population[i+1].fitness )
      {
        best = population[i+1].fitness;
        best_mem = i + 1;
      }

    }

  }
// 
//  If the best individual from the new population is better than 
//  the best individual from the previous population, then 
//  copy the best from the new population; else replace the 
//  worst individual from the current population with the 
//  best one from the previous generation                     
//
  if ( population[POPSIZE].fitness <= best )
  {
    for ( i = 0; i < NVARS; i++ )
    {
      population[POPSIZE].gene[i] = population[best_mem].gene[i];
    }
    population[POPSIZE].fitness = population[best_mem].fitness;
    population[POPSIZE].K = population[best_mem].K;

  }
  else
  {
    for ( i = 0; i < NVARS; i++ )
    {
      population[worst_mem].gene[i] = population[POPSIZE].gene[i];
    }
    population[worst_mem].fitness = population[POPSIZE].fitness;
    population[worst_mem].K = population[POPSIZE].K;
  } 

  return;
}
//****************************************************************************80

void evaluate ( )

//****************************************************************************80
// 
//  Purpose:
//
//    EVALUATE implements the user-defined valuation function
//
//  Discussion:
//
//    Each time this is changed, the code has to be recompiled.
//    The current function is:  x[1]^2-x[1]*x[2]+x[3]
//
//  Licensing:
//
//    This code is distributed under the GNU LGPL license. 
//
//  Modified:
//
//    29 December 2007
//
//  Author:
//
//    Original version by Dennis Cormier and Sita Raghavan.
//    This C++ version by John Burkardt.
//
{
  int member;
  int i;

  for ( member = 0; member < POPSIZE; member++ ) {
    /*
    create_indicators(population[member].gene[0], population[member].gene[1]);
    int Kmax = nbNoises.size();
    vector< double > eval (Kmax);


    double maxi = -10000000;
    for (int k = 0; k < Kmax; k++){
      eval[k] = population[member].gene[2] * nbRealCurves[k] - population[member].gene[3] * nbNoises[k];
      //cerr << k << " " << eval[k];
      if (eval[k] > maxi)
        maxi = eval[k];
    }
    //cerr << endl;
    for (int k = 0; k < Kmax; k++)
      eval[k] /= maxi;

    double bestScore, bestK;
    bestScore = /*eval[0] - eval[1] eval[0];
    //cerr << eval[0] - eval[1] << " ";
    bestK = 0;
    for (int k = 1; k < Kmax -1; k++) {
      //cerr << 2*eval[k] - eval[k-1] - eval[k+1] <<" ";
      if (/*2*eval[k] - eval[k-1] - eval[k+1] eval[k] > bestScore) {
        bestScore = 2*eval[k]  /2/*- eval[k-1] - eval[k+1];
        bestK = k;
      }
      //cerr << k << " " << 2*eval[k] - eval[k-1] - eval[k+1] << endl;
    }
    //cerr << eval[Kmax-1] - eval[Kmax-2] << endl;
    if (/*eval[Kmax-1] - eval[Kmax-2] eval[Kmax-1] > bestScore) {
      bestScore = eval[Kmax-1] /*- eval[Kmax-2];
      bestK = Kmax-1;      
    }

    //cerr << bestScore << " " << bestK << endl;*/

    double bestScore = -1000000000;
    double bestK = -1;

    cout << bestScore << endl;
    cout <<  "  "<<   population[member].gene[0] <<" * "<< meanNbPoints[0] << endl
       <<  "+ "<<   population[member].gene[1] <<"*"<< meanDist1[0] <<endl
       <<  "+ "<<   population[member].gene[2] <<"*"<< meanDist2[0] <<endl
       <<  "- "<<   population[member].gene[3] <<"*"<< nbCurves[0]<<endl << endl << endl;
    
    for (int k = 0; k < nbCurves.size(); k++) {
      double score =     population[member].gene[0] * meanNbPoints[0] 
                       + population[member].gene[1] * meanDist1[0] 
                       + population[member].gene[2] * meanDist2[0] 
                       - population[member].gene[3] * nbCurves[0];
      cout << score << endl;
      cout <<  "  "<<   population[member].gene[0] <<" * "<< meanNbPoints[k] << endl
           <<  "+ "<<   population[member].gene[1] <<"*"<< meanDist1[k] <<endl
           <<  "+ "<<   population[member].gene[2] <<"*"<< meanDist2[k] <<endl
           <<  "- "<<   population[member].gene[3] <<"*"<< nbCurves[k]<<endl << endl << endl;
      
      if (score > bestScore) {
        bestScore = score;
        bestK = k;
      }
    }

    population[member].fitness = bestScore;
    population[member].K = bestK;
    //cerr << member << " " << bestScore << " " << bestK << endl;
  }
  return;
}
//****************************************************************************80

int i4_uniform_ab ( int a, int b, int &seed )

//****************************************************************************80
//
//  Purpose:
//
//    I4_UNIFORM_AB returns a scaled pseudorandom I4 between A and B.
//
//  Discussion:
//
//    The pseudorandom number should be uniformly distributed
//    between A and B.
//
//  Licensing:
//
//    This code is distributed under the GNU LGPL license. 
//
//  Modified:
//
//    02 October 2012
//
//  Author:
//
//    John Burkardt
//
//  Reference:
//
//    Paul Bratley, Bennett Fox, Linus Schrage,
//    A Guide to Simulation,
//    Second Edition,
//    Springer, 1987,
//    ISBN: 0387964673,
//    LC: QA76.9.C65.B73.
//
//    Bennett Fox,
//    Algorithm 647:
//    Implementation and Relative Efficiency of Quasirandom
//    Sequence Generators,
//    ACM Transactions on Mathematical Software,
//    Volume 12, Number 4, December 1986, pages 362-376.
//
//    Pierre L'Ecuyer,
//    Random Number Generation,
//    in Handbook of Simulation,
//    edited by Jerry Banks,
//    Wiley, 1998,
//    ISBN: 0471134031,
//    LC: T57.62.H37.
//
//    Peter Lewis, Allen Goodman, James Miller,
//    A Pseudo-Random Number Generator for the System/360,
//    IBM Systems Journal,
//    Volume 8, Number 2, 1969, pages 136-143.
//
//  Parameters:
//
//    Input, int A, B, the limits of the interval.
//
//    Input/output, int &SEED, the "seed" value, which should NOT be 0.
//    On output, SEED has been updated.
//
//    Output, int I4_UNIFORM, a number between A and B.
//
{
  int c;
  const int i4_huge = 2147483647;
  int k;
  float r;
  int value;

  if ( seed == 0 )
  {
    cerr << "\n";
    cerr << "I4_UNIFORM_AB - Fatal error!\n";
    cerr << "  Input value of SEED = 0.\n";
    exit ( 1 );
  }
//
//  Guarantee A <= B.
//
  if ( b < a )
  {
    c = a;
    a = b;
    b = c;
  }

  k = seed / 127773;

  seed = 16807 * ( seed - k * 127773 ) - k * 2836;

  if ( seed < 0 )
  {
    seed = seed + i4_huge;
  }

  r = ( float ) ( seed ) * 4.656612875E-10;
//
//  Scale R to lie between A-0.5 and B+0.5.
//
  r = ( 1.0 - r ) * ( ( float ) a - 0.5 ) 
    +         r   * ( ( float ) b + 0.5 );
//
//  Use rounding to convert R to an integer between A and B.
//
  value = round ( r );
//
//  Guarantee A <= VALUE <= B.
//
  if ( value < a )
  {
    value = a;
  }
  if ( b < value )
  {
    value = b;
  }

  return value;
}
//****************************************************************************80

void initialize ( string filename, int &seed )

//****************************************************************************80
// 
//  Purpose:
//
//    INITIALIZE initializes the genes within the variables bounds. 
//
//  Discussion:
//
//    It also initializes (to zero) all fitness values for each
//    member of the population. It reads upper and lower bounds 
//    of each variable from the input file `gadata.txt'. It 
//    randomly generates values between these bounds for each 
//    gene of each genotype in the population. The format of 
//    the input file `gadata.txt' is 
//
//      var1_lower_bound var1_upper bound
//      var2_lower_bound var2_upper bound ...
//
//  Licensing:
//
//    This code is distributed under the GNU LGPL license. 
//
//  Modified:
//
//    28 April 2014
//
//  Author:
//
//    Original version by Dennis Cormier and Sita Raghavan.
//    This C++ version by John Burkardt.
//
//  Parameters:
//
//    Input, string FILENAME, the name of the input file.
//
//    Input/output, int &SEED, a seed for the random number generator.
//
{
  int i;
  ifstream input;
  int j;
  double lbound;
  double ubound;

  input.open ( filename.c_str ( ) );

  if ( !input )
  {
    cerr << "\n";
    cerr << "INITIALIZE - Fatal error!\n";
    cerr << "  Cannot open the input file!\n";
    exit ( 1 );
  }
// 
//  Initialize variables within the bounds 
//
  for ( i = 0; i < NVARS; i++ )
  {
    input >> lbound >> ubound;

    for ( j = 0; j < POPSIZE; j++ )
    {
      population[j].fitness = -10e12;
      population[j].K = -1;
      population[j].rfitness = 0;
      population[j].cfitness = 0;
      population[j].lower[i] = lbound;
      population[j].upper[i]= ubound;
      population[j].gene[i] = r8_uniform_ab ( lbound, ubound, seed );
    }
  }

  input.close ( );

  return;
}
//****************************************************************************80

void keep_the_best ( )

//****************************************************************************80
// 
//  Purpose:
//
//    KEEP_THE_BEST keeps track of the best member of the population. 
//
//  Discussion:
//
//    Note that the last entry in the array Population holds a 
//    copy of the best individual.
//
//  Licensing:
//
//    This code is distributed under the GNU LGPL license. 
//
//  Modified:
//
//    29 December 2007
//
//  Author:
//
//    Original version by Dennis Cormier and Sita Raghavan.
//    This C++ version by John Burkardt.
//
//  Local parameters:
//
//    Local, int CUR_BEST, the index of the best individual.
//
{
  int cur_best;
  int mem;
  int i;

  cur_best = 0;

  for ( mem = 0; mem < POPSIZE; mem++ )
  {
    if ( population[POPSIZE].fitness < population[mem].fitness )
    {
      cur_best = mem;
      population[POPSIZE].fitness = population[mem].fitness;
      population[POPSIZE].K = population[mem].K;
    }
  }
  population[POPSIZE].fitness = -10e12;
// 
//  Once the best member in the population is found, copy the genes.
//
  for ( i = 0; i < NVARS; i++ )
  {
    population[POPSIZE].gene[i] = population[cur_best].gene[i];
  }

  return;
}
//****************************************************************************80

void mutate ( int &seed )

//****************************************************************************80
// 
//  Purpose:
//
//    MUTATE performs a random uniform mutation. 
//
//  Discussion:
//
//    A variable selected for mutation is replaced by a random value 
//    between the lower and upper bounds of this variable.
//
//  Licensing:
//
//    This code is distributed under the GNU LGPL license. 
//
//  Modified:
//
//    28 April 2014
//
//  Author:
//
//    Original version by Dennis Cormier and Sita Raghavan.
//    This C++ version by John Burkardt.
//
//  Parameters:
//
//    Input/output, int &SEED, a seed for the random number generator.
//
{
  const double a = 0.0;
  const double b = 1.0;
  int i;
  int j;
  double lbound;
  double ubound;
  double x;

  for ( i = 0; i < POPSIZE; i++ )
  {
    for ( j = 0; j < NVARS; j++ )
    {
      x = r8_uniform_ab ( a, b, seed );
      if ( x < PMUTATION )
      {
        lbound = population[i].lower[j];
        ubound = population[i].upper[j];  
        population[i].gene[j] = r8_uniform_ab ( lbound, ubound, seed );
      }
    }
  }

  return;
}
//****************************************************************************80

double r8_uniform_ab ( double a, double b, int &seed )

//****************************************************************************80
//
//  Purpose:
//
//    R8_UNIFORM_AB returns a scaled pseudorandom R8.
//
//  Discussion:
//
//    The pseudorandom number should be uniformly distributed
//    between A and B.
//
//  Licensing:
//
//    This code is distributed under the GNU LGPL license. 
//
//  Modified:
//
//    09 April 2012
//
//  Author:
//
//    John Burkardt
//
//  Parameters:
//
//    Input, double A, B, the limits of the interval.
//
//    Input/output, int &SEED, the "seed" value, which should NOT be 0.
//    On output, SEED has been updated.
//
//    Output, double R8_UNIFORM_AB, a number strictly between A and B.
//
{
  int i4_huge = 2147483647;
  int k;
  double value;

  if ( seed == 0 )
  {
    cerr << "\n";
    cerr << "R8_UNIFORM_AB - Fatal error!\n";
    cerr << "  Input value of SEED = 0.\n";
    exit ( 1 );
  }

  k = seed / 127773;

  seed = 16807 * ( seed - k * 127773 ) - k * 2836;

  if ( seed < 0 )
  {
    seed = seed + i4_huge;
  }

  value = ( double ) ( seed ) * 4.656612875E-10;

  value = a + ( b - a ) * value;

  return value;
}
//****************************************************************************80

void report ( int generation )

//****************************************************************************80
// 
//  Purpose:
//
//    REPORT reports progress of the simulation. 
//
//  Licensing:
//
//    This code is distributed under the GNU LGPL license. 
//
//  Modified:
//
//    29 December 2007
//
//  Author:
//
//    Original version by Dennis Cormier and Sita Raghavan.
//    This C++ version by John Burkardt.
//
//  Local parameters:
//
//    Local, double avg, the average population fitness.
//
//    Local, best_val, the best population fitness.
//
//    Local, double square_sum, square of sum for std calc.
//
//    Local, double stddev, standard deviation of population fitness.
//
//    Local, double sum, the total population fitness.
//
//    Local, double sum_square, sum of squares for std calc.
//
{
  double avg;
  double best_val;
  int i;
  double square_sum;
  double stddev;
  double sum;
  double sum_square;
  int best_K;
  if ( generation == 0 )
  {
    cout << "\n";
    cout << "  Generation       Best            Average       Standard        Best K \n";
    cout << "  number           value           fitness       deviation       Yet \n";
    cout << "\n";
  }

  sum = 0.0;
  sum_square = 0.0;

  for ( i = 0; i < POPSIZE; i++ )
  {
    sum = sum + population[i].fitness;
    sum_square = sum_square + population[i].fitness * population[i].fitness;
  }

  avg = sum / ( double ) POPSIZE;
  square_sum = avg * avg * POPSIZE;
  stddev = sqrt ( ( sum_square - square_sum ) / ( POPSIZE - 1 ) );
  best_val = population[POPSIZE].fitness;
  best_K = population[POPSIZE].K;

  cout << "  " << setw(8) << generation 
       << "  " << setw(14) << best_val 
       << "  " << setw(14) << avg 
       << "  " << setw(14) << stddev
       << "  " << setw(14) << best_K << "\n";

  return;
}
//****************************************************************************80

void selector ( int &seed )

//****************************************************************************80
// 
//  Purpose:
//
//    SELECTOR is the selection function.
//
//  Discussion:
//
//    Standard proportional selection for maximization problems incorporating 
//    the elitist model.  This makes sure that the best member always survives.
//
//  Licensing:
//
//    This code is distributed under the GNU LGPL license. 
//
//  Modified:
//
//    28 April 2014
//
//  Author:
//
//    Original version by Dennis Cormier and Sita Raghavan.
//    This C++ version by John Burkardt.
//
//  Parameters:
//
//    Input/output, int &SEED, a seed for the random number generator.
//
{
  const double a = 0.0;
  const double b = 1.0;
  int i;
  int j;
  int mem;
  double p;
  double sum;
//
//  Find the total fitness of the population.
//
  sum = 0.0;
  for ( mem = 0; mem < POPSIZE; mem++ )
  {
    sum = sum + population[mem].fitness;
  }
//
//  Calculate the relative fitness of each member.
//
  for ( mem = 0; mem < POPSIZE; mem++ )
  {
    population[mem].rfitness = population[mem].fitness / sum;
  }
// 
//  Calculate the cumulative fitness.
//
  population[0].cfitness = population[0].rfitness;
  for ( mem = 1; mem < POPSIZE; mem++ )
  {
    population[mem].cfitness = population[mem-1].cfitness +       
      population[mem].rfitness;
  }
// 
//  Select survivors using cumulative fitness. 
//
  for ( i = 0; i < POPSIZE; i++ )
  { 
    p = r8_uniform_ab ( a, b, seed );
    if ( p < population[0].cfitness )
    {
      newpopulation[i] = population[0];      
    }
    else
    {
      for ( j = 0; j < POPSIZE; j++ )
      { 
        if ( population[j].cfitness <= p && p < population[j+1].cfitness )
        {
          newpopulation[i] = population[j+1];
        }
      }
    }
  }
// 
//  Overwrite the old population with the new one.
//
  for ( i = 0; i < POPSIZE; i++ )
  {
    population[i] = newpopulation[i]; 
  }

  return;     
}
//****************************************************************************80

void timestamp ( )

//****************************************************************************80
//
//  Purpose:
//
//    TIMESTAMP prints the current YMDHMS date as a time stamp.
//
//  Example:
//
//    May 31 2001 09:45:54 AM
//
//  Licensing:
//
//    This code is distributed under the GNU LGPL license. 
//
//  Modified:
//
//    04 October 2003
//
//  Author:
//
//    John Burkardt
//
{
# define TIME_SIZE 40

  static char time_buffer[TIME_SIZE];
  const struct tm *tm;
  size_t len;
  time_t now;

  now = time ( NULL );
  tm = localtime ( &now );

  len = strftime ( time_buffer, TIME_SIZE, "%d %B %Y %I:%M:%S %p", tm );

  cout << time_buffer << "\n";

  return;
# undef TIME_SIZE
}
//****************************************************************************80

void Xover ( int one, int two, int &seed )

//****************************************************************************80
// 
//  Purpose:
//
//    XOVER performs crossover of the two selected parents. 
//
//  Licensing:
//
//    This code is distributed under the GNU LGPL license. 
//
//  Modified:
//
//    28 April 2014
//
//  Author:
//
//    Original version by Dennis Cormier and Sita Raghavan.
//    This C++ version by John Burkardt.
//
//  Local parameters:
//
//    Local, int point, the crossover point.
//
//  Parameters:
//
//    Input, int ONE, TWO, the indices of the two parents.
//
//    Input/output, int &SEED, a seed for the random number generator.
//
{
  int i;
  int point;
  double t;
// 
//  Select the crossover point.
//
  point = i4_uniform_ab ( 0, NVARS - 1, seed );
//
//  Swap genes in positions 0 through POINT-1.
//
  for ( i = 0; i < point; i++ )
  {
    t                       = population[one].gene[i];
    population[one].gene[i] = population[two].gene[i];
    population[two].gene[i] = t;
  }

  return;
}
