[AC Analysis]
{
   Npanes: 1
   {
      traces: 1 {524290,0,"V(out)/V(inj)"}
      X: ('M',0,1,0,1e+07)
      Y[0]: (' ',0,0.0001,20,10000)
      Y[1]: (' ',0,-180,45,180)
      Log: 1 2 0
      GridStyle: 1
      PltMag: 1
      PltPhi: 1 1
   }
}
[Transient Analysis]
{
   Npanes: 1
   {
      traces: 1 {524290,0,"V(5vref_pwm_avg)"}
      X: ('m',0,0,0.003,0.027)
      Y[0]: (' ',2,4.82,0.02,5.08)
      Y[1]: ('_',0,1e+308,0,-1e+308)
      Volts: (' ',0,0,1,4.82,0.02,5.08)
      Log: 0 0 0
      GridStyle: 1
   }
}
