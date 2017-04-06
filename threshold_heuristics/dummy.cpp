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



struct point {
  int x; int y;
};

vector< vector<point> > data;


//vector< double > nbRealCurves;
//vector< double > nbNoises; 
//vector< vector<double> > brutRepli;


int main (int argc, char* argv[]);
void evaluate ( );

/*
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
      cout << endl << endl << endl;
      cout << nbCurves[K] << " " <<
      meanNbPoints[K] <<" " <<
      meanDist1[K] << " " <<
      meanDist2[K] << endl;
       
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
}*/

vector< double > eval;
vector< double> nbPoints;
vector< double > nbCurves;

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
      nbPoints.push_back(0);
      
      for (int c = 0; c < data.size(); c++) {
        nbPoints[K] += data[c].size();
      }
      nbCurves[K] = data.size();
       
      data.clear();
      K++;
      cout << K << " done" << endl;

    }
  }
  /*
  double maxNbCurves (0), maxNbPoints (0);
  for (int k = 0; k < nbCurves.size(); k++) {
    maxNbCurves = max(maxNbCurves, nbCurves[k]);
    maxNbPoints = max(maxNbPoints, nbPoints[k]);
    cerr << k << " " << nbCurves[k] << " " << nbPoints[k] << endl;
  }
  for (int k = 0; k < nbCurves.size(); k++) {
    nbCurves[k] /= maxNbCurves;
    nbPoints[k] /= maxNbPoints;
  }
  */

}



int main (int argc, char* argv[])
{
  string dataToAnalyse = argv[1];


  


  read_file(dataToAnalyse);


  evaluate ( );



  return 0;
}

void evaluate ( )
{
  int rappA (10), rappB (1);
  for (int i = 0; i < nbCurves.size(); i++) {
    eval.push_back(rappB*nbPoints[i] - rappA*nbCurves[i]);
    cerr << i << " " << nbPoints[i] << " " << nbCurves[i] << endl;
  }

  double evalMax = eval[0];
  int ind = 0;
  for (int i = 1; i < eval.size(); i++) {
    if (eval[i] > evalMax) {
      evalMax = eval[i];
      ind = i;
    }
  }
  cout << "Best K : " << ind << endl;
}
