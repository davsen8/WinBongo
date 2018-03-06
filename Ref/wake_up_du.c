/*************************************************************************/
/* ROUTINE TO WAKE UP ctd BY SENDING STREAM OF cr-lf'S UNTIL IT RESPONDS */
/* WITH A S> PROMPT. IF MORE THAN 70 ATTEMPTS MADE AN ERROR IS ASSUMED.  */
/*************************************************************************/

int wake_up_du (port,issue_error)

int port ;
int issue_error;
{
int run,i,j,C ;

j=0 ; run = YES ; C ='\0' ;
asiclear (port,ASINOUT) ;

asiputc(port,13);
timer(1);
asiputc(port,13);
timer(1);

while (run && (j<=20)) 
{ 
 asiputc(port,13);
 j++;i=5;
 while ( isrxempty(port) && ((i--) > 0) ) timer(4);

 while (!isrxempty(port) && run)
   {
    C = asigetc(port);
    timer(1);
          if (C =='S')
                { if (!isrxempty(port));
                  if (asigetc(port) =='>')
                     run=NO;
                }
   }     

if (kbhit())    /* operator Abort */
   if (getkey() == 27)
    { run = NO; j=27; issue_error = NO; }
}   
if (j>20)
 {
   if (issue_error)
    {
      putchar(7) ;puts(hires);
      frame (15,19,18,60);
      outhi (16,19," *** TIME OUT ERROR WAKING UP CTD !! *** ") ;
      outhi (17,19,"    CHECK CABLE CONNECTIONS AND RETRY..  ");
      outhi (18,19,"   PRESS ANY KEY TO RETURN TO MAIN MENU. ");
      getkey();puts(lores);
    }
    asiclear(port,ASINOUT);
    return (NO);
 }
else
 { asiclear(port,ASINOUT);
  return (YES);
 }
}

/**********************************************************************/
