[Transient Analysis]
{
   Npanes: 1
   {
      traces: 1 {268959746,0,"V(p15v_pri)"}
      X: (' ',2,8.84,0.04,9.24)
      Y[0]: (' ',1,15,0.1,16.5)
      Y[1]: ('_',0,1e+308,0,-1e+308)
      Volts: (' ',0,0,0,15,0.1,16.5)
      Log: 0 0 0
      GridStyle: 1
   }
}
[AC Analysis]
{
   Npanes: 1
   {
      traces: 1 {2,0,"V(p15v_pri)/V(inj)"}
      X: ('M',0,10,99999,1e+06)
      Y[0]: (' ',0,0.0001,20,10000)
      Y[1]: (' ',0,-180,45,180)
      Log: 1 2 0
      GridStyle: 1
      PltMag: 1
      PltPhi: 1 0
   }
}
