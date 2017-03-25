#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <stdio.h>      /* printf, scanf, puts, NULL */
#include <stdlib.h>     /* srand, rand */
#include <time.h>  
#include <ctype.h>
#include<vector>
using namespace std;
using namespace cv;

struct tree
{
	int parent;
	int next;
	int firstchild;
	int previous;
};

bool fstcheckfct(FILE* fout, Mat image, Point2f p, vector<Point2f> contour)
{
	int res = pointPolygonTest(contour, p, false);
		if(res==1)
		{
			for(int i=0;i<3;i++)
				fprintf(fout,"%d ", (image.at<Vec3b>(p.y,p.x))[i]);
			fprintf(fout,"\n");
			return true;
		}
		return false;
};


/*
 * This is how to check if a point is in on or out of the polygon 
 * res = pointPolygonTest(contour, pt, false);
 * contour is the contour of type inputArray
 * pt is the point to check
 *
 */
int readinput(vector<vector<Point2f> >& vec2 , vector<struct tree> hierarchy)
{
  char character='#';
  bool endContour = false;
  bool doubleSharp = false;
  int x,y;
  vector<Point2f> vec;	// vec is a contour, a vector of points
  while(character=='#')
		scanf("%c",&character);
  while(!doubleSharp)
	{
		while(!endContour)
		{
			character=getchar();
			if(character=='#')
			{
				endContour=true;
				character=getchar();
				if(character=='#');
					doubleSharp=true;
			}
			else if(isdigit(character))
			{
				ungetc(character,stdin);
				scanf("%d", &y);
				getchar();
				scanf("%d", &x);
				printf("x %d y %d \n",x,y);
				vec.push_back(Point2f(y,x));				
			}
		}
		vec2.push_back(vec);
		endContour=false;
		vec.clear();
	}
	int N;
	character='#';
	while(!isdigit(character)) character=getchar();
	ungetc(character,stdin);
	scanf("%d",&N); /* We suppose N is given before the hierarchy after the contours, if not, tell Remi to add it, he said it's OK if need be */
	printf("N is read as %d\n",N);
	for(int i=0;i<N;i++)
	{
		struct tree a;
		scanf("%d",&(a.next));
		scanf("%d",&(a.previous));
		scanf("%d",&(a.firstchild));
		scanf("%d",&(a.parent));
		hierarchy.push_back(a);
	} /* hierarchy is read */
	return N;
}

int main(int argc, char** argv)
{
	vector<vector<Point2f> > vec2; // vec2 is a vector of contours
	vector<struct tree> hierarchy;
	
	FILE *fout=fopen("colors.txt","w");
	double res, ey, ex, sy, sx, ry, rx, alpha=1, x, y;			//result
	//first step: we need to have an array contour filled with the contour according to the drawing on my feuille.
	int*** contour;
	//TODO
	int number_of_contour=readinput(vec2, hierarchy);
	//end of first step: contour is filled with the data.


	//TODO
		Mat image= imread(argv[1]);
	//END of TODO
	
	int c=0;
	while(c<number_of_contour) //the input arrays are separated by #
	{		
		int number_of_points_in_contour=(sizeof(contour[c])/sizeof(*contour[c]));
		bool found=false;
		int currentpoint=0;
		while(!found && currentpoint<3*(number_of_points_in_contour/3))
		{
			if(fstcheckfct(fout, image, Point2f(vec2[c][currentpoint].y+1,vec2[c][currentpoint].x+1),vec2[c]))
				found=true;
			else if(fstcheckfct(fout, image, Point2f(vec2[c][currentpoint].y-1,vec2[c][currentpoint].x+1),vec2[c]))
				found=true;
			else if(fstcheckfct(fout, image, Point2f(vec2[c][currentpoint].y-1,vec2[c][currentpoint].x-1),vec2[c]))
				found=true;
			else if(fstcheckfct(fout, image, Point2f(vec2[c][currentpoint].y+1,vec2[c][currentpoint].x-1),vec2[c]))
				found=true;
			else
				currentpoint+=number_of_points_in_contour/3;
		}
		if(!found)
		{		
		//compute the mean of y in contour assign it to ey
		//compute the mean of x, assign it to ex
		ey=0;
		ex=0;
		int p=0;
		for(p=0;p<number_of_points_in_contour;p++){
			ey+=vec2[c][p].y;
			ex+=vec2[c][p].x;
		}
		ey=ey/number_of_points_in_contour;
		ex=ex/number_of_points_in_contour;

		//compute the standard deviation in x assign it to sx
		//compute the standard deviation in y assign it to sy
		sx=0;
		sy=0;

		for(p=0;p<number_of_points_in_contour;++p){
			sx+=(ex-vec2[c][p].x)*(ex-vec2[c][p].x);
			sy+=(ey-vec2[c][p].y)*(ey-vec2[c][p].y);
		}

		sx=sqrt(sx);
		sy=sqrt(sy);

		//detection

		srand(time(NULL)); //init random number generator
		rx=ry=0;

		while(pointPolygonTest(vec2[c], Point2f(ey+ry,ex+rx), false)<1)//TODO
		{
			printf("HEEY\n");
			//pick a random float between -alpha*sx and alpha*sx, assign it to rx
			rx = static_cast <double> (rand()) / static_cast <double> (RAND_MAX/(2*alpha*sx));		
			rx-=alpha*sx;
			//equivalent for ry
			ry = static_cast <double> (rand()) / static_cast <double> (RAND_MAX/(2*alpha*sy));
			ry-=alpha*sy;
		}
		//write out the color of this point followed by newline # newline
		for(int i=0;i<3;i++)
		{
				fprintf(fout,"%d ", image.at<Vec3b>(ey+ry,ex+rx)[i]);
		}		
		fprintf(fout,"\n");
		++c;
	}
	}
	return 0;
}
