/***************************/
/*****  COMPUTE DEPTH ******/
/***************************/

 /* compute depth in meters from pressure in decibars */
 /* using saunders and fofnoff's method */
 /* deep sea research 1976,23,109-111 */
double cal_depth (double p)
 {
  double x,gr,latitude = 47.0; /* nominal value */
  double depth  ;

  x = sin(latitude / 57.29578);
  x = x * x;
  gr = 9.780318 * (1.000 + (5.2788e-3 + 2.36e-5 * x) * x) + 1.092e-6 * p;
  depth = ((((-1.82e-15 * p + 2.279e-10) * p - 2.2512e-5) * p + 9.72659)*p)/gr;
  return (depth);
}