[Transient Analysis]
{
   Npanes: 1
   {
      traces: 1 {268959747,0,"V(n042)"}
      X: ('m',0,0,0.001,0.012)
      Y[0]: ('m',0,0,0.04,0.4)
      Y[1]: ('n',1,1e+308,2e-10,-1e+308)
      Volts: ('m',0,0,0,0,0.04,0.4)
      Log: 0 0 0
      GridStyle: 1
   }
}
[AC Analysis]
{
   Npanes: 1
   {
      traces: 4 {2,0,"V(out)/V(inj)"} {3,0,"V(COMP)/V(OPTO_OUT)"} {4,0,"I(ROUT_OPTO)/I(RIN_OPTO)"} {5,0,"V(OUT)/V(COMP)"}
      X: ('M',0,1,0,1e+07)
      Y[0]: (' ',0,0.0001,20,10000)
      Y[1]: (' ',0,-180,45,180)
      Log: 1 2 0
      GridStyle: 1
      PltMag: 1
      PltPhi: 1 1
   }
}
