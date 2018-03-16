import wx


class IntRangeValidator(wx.PyValidator):
     """ This validator is used to check integer values between a range
     """
     def __init__(self,minflag,maxflag):
#     def __init__(self):
          """ standard contructor - intialize the validator.
          """
#          wx.PyValidator.__init__(self)
          self.minflag = minflag
          self.maxflag = maxflag
          super(IntRangeValidator, self).__init__()

# Event mangement
          self.Bind(wx.EVT_CHAR, self.OnChar) 

          self._min = int(self.minflag)
          self._max = int(self.maxflag)


     def Clone(self):
          """ Standard cloner. a required override

             Note that every validator must implement the Clone() method.
          """

          return IntRangeValidator(self.minflag,self.maxflag)



     def Validate(self, win):
         """ Validate the contents of the given text control. overrider
         """
# this is activated by the ok button

         txtCtrl = self.GetWindow()
         val = txtCtrl.GetValue()
         if val =='':
               return
          
         isValid = True
#         if val.isdigit():
#          digit=int(val)
# deal with a minus sign , and make sure it can only be in position 1 if follwed by a number
# this is due to ability to enter a - then tab off the field getting by the OnChar test

         if len(val)==1 and val[0]=='-':
            isValid = False 
            fnum = self._min
            baddigit = val[0]
         else:
          fnum=float(val)  
     
          if (fnum >=self._min and fnum <= self._max-10):
               isValid = True
          else :
               baddigit = str(digit)
               isValid=False
               
         if not isValid :
          # pop up a message
          msg = "value must be between %d and %d not %s"  % \
                 (self._min, self._max,baddigit)
          wx.MessageBox (msg,"Invalid value",style=wx.OK|wx.ICON_ERROR)
#          txtCtrl.SetValue("")
          
         return isValid
          
     def OnChar(self, event):

          txtCtrl  = self.GetWindow()
          id = txtCtrl.GetId()

          key = event.GetKeyCode()

          isDigit = False
          if key < 256 :
               isDigit = chr(key).isdigit()
# pass through a minus (9) or deciml place (.).. need to find or define a isanumber element function
          if key == 45 or key==46:
             isDigit = True

          if key in (wx.WXK_RETURN,wx.WXK_DELETE,wx.WXK_BACK) or key > 255 or isDigit:
               if isDigit:
                    #Check if in Range

#getval returns what is entered upto but NOT including the current key pressed
                    val = txtCtrl.GetValue()

                    digit = chr(key)
                    pos = txtCtrl.GetInsertionPoint()
                    # add current key enter to others then check for value in range
                    if pos == len(val):
                         val += digit
                    else:
                         val = val[:pos] + digit + val[pos:]

                    err=False

                    if (digit =='.')or((digit=='-' or digit=='0') and pos==0):
                        err= False 
                        fval = self._min                 
                    elif (digit=='-' and pos>0):
                        err=True
                        fval =-1
                    else:
                      fval = float(val)
                      
                    if err or (fval < self._min or fval > self._max):
                      if not wx.Validator_IsSilent():
                        wx.Bell()
                        msg = "value must be between %d and %d val is %s" % \
                 (self._min, self._max,val)
                        wx.MessageBox (msg,"Invalid value",style=wx.OK|wx.ICON_ERROR)
                      return  
                   
               event.Skip()
               return
          
          if not wx.Validator_IsSilent():
               wx.Bell()
               msg = "tumble tru value must be between %d and %d" % \
                 (self._min, self._max)
               wx.MessageBox (msg,"Invalid value",style=wx.OK|wx.ICON_ERROR)

     
 
 
     def TransferToWindow(self):
         """ Transfer data from validator to window.

             The default implementation returns False, indicating that an error
             occurred.  We simply return True, as we don't do any data transfer.
         """
         return True # Prevent wxDialog from complaining.


     def TransferFromWindow(self):
         """ Transfer data from window to validator.

             The default implementation returns False, indicating that an error
             occurred.  We simply return True, as we don't do any data transfer.
         """
         return True
 # Prevent wxDialog from complaining.

#----------------------------------------------------------------------
