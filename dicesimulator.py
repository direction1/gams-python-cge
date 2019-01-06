#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 20:08:26 2019

@author: danluo
"""

from __future__ import print_function
from gams import *
import sys

def get_model_text(iteration, datadict):
    return '''

*display tindex;
snowfeed = {:s};
miunowfeed = {:s};
tt(t) = yes$(t.val eq {:s});
alias(t,ttt);
*display MAT(t)$(t.val );
loop(ttt$tt(ttt),
           etreenow       = etree(ttt);
           sigmanow     = sigma(ttt);
           forcothnow   = forcoth(ttt);
           cost1now     = cost1(ttt);
           partfractnow = partfract(ttt);
           pbacktimenow = pbacktime(ttt);
           epsilontnow  = epsilont(ttt);
           alnow        = al(ttt);
           Lnow         = L(ttt);
           Yepsilonnow  = Yepsilon(ttt);
           rrnow        = rr(ttt);

         MIUnow.up       = limmiu*partfractnow;
         Know.LO         = 1;

         MATnow.LO       = 10;
         MUnow.LO        = 100;
         MLnow.LO        = 1000;
         Cnow.LO         = 2;
         TOCEANnow.UP    = 20;
         TOCEANnow.LO    = -1;
         TATMnow.UP      = 40;
         CPCnow.LO      = .01;

         Knext.LO         = 1;
         MATnext.LO       = 10;
         MUnext.LO        = 100;
         MLnext.LO        = 1000;
         TOCEANnext.UP    = 20;
         TOCEANnext.LO    = -1;
         TATMnext.UP      = 40;
         CCAnow.up       = fosslim;
         CCAnext.up       = fosslim;


           MATnow.fx       = {:s};
           MLnow.fx        = {:s};
           MUnow.fx        = {:s};
           TATMnow.fx      = {:s};
           TOCEANnow.fx    = {:s};
           CCAnow.fx       = {:s};
           Know.fx         = {:s};
*           Snow.fx         = 0.06;
*           miunow.fx          = 0.01;
MIUnow.up$(ttt.val<30) = 1;
Snow.FX$(ttt.val>50) = optlrsav;

* Base carbon price if base, otherwise optimized
* Warning: If parameters are changed, the next equation might make base case infeasible.
* If so, reduce tnopol so that don't run out of resources.
cpricenow.up$(ifopt=0) = cpricebase(ttt);
cpricenow.up$(ttt.val>tnopol) = 1000;
cpricenow.up$(ttt.val=1)=cpricebase('1');
snowfeed = 1;
miunowfeed = 1;

)
solve co2 minimize dummy using nlp;


 '''.format(str(datadict['snowfeed']),str(datadict['miunowfeed']),str(iteration),
 'MAT(ttt)' if iteration==1 else str(datadict['MATnext']),
 'ML(ttt)' if iteration==1 else str(datadict['MLnext']),
 'Mu(ttt)' if iteration==1 else str(datadict['Munext']),
 'TATM(ttt)' if iteration==1 else str(datadict['TATMnext']),
 'TOCEAN(ttt)' if iteration==1 else str(datadict['TOCEANnext']),
 'CCA(ttt)' if iteration==1 else str(datadict['CCAnext']),
 'K(ttt)' if iteration==1 else str(datadict['Knext']))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ws = GamsWorkspace(system_directory = sys.argv[1])
    else:
        ws = GamsWorkspace()

    cp = ws.add_checkpoint()

    # initialize a GAMSCheckpoint by running a GAMSJob
    t5 = ws.add_job_from_file("/Users/danluo/Documents/gamsdir/projdir/Untitled_2.gms")
    t5.run(checkpoint=cp)
    datadict={};
    datadict['snowfeed'] = 1;
    datadict['miunowfeed']=1;
    datadict['MATnext'] = 866;
    datadict['MLnext'] = 10010.4;
    datadict['Munext'] = 1541.1;
    datadict['TATMnext'] = 0;
    datadict['TOCEANnext'] = 0.0266;
    datadict['CCAnext'] = 135.76;
    datadict['Knext'] = 387.1;
    iteration = 1;
#    print(get_model_text(iteration, datadict));
#    import pdb;pdb.set_trace();
    


    # create a new GAMSJob that is initialized from the GAMSCheckpoint
#    import datetime
#    starttime = datetime.datetime.now()
    for iteration in range(2,3):
        t5 = ws.add_job_from_string(get_model_text(iteration, datadict), cp)
        t5.run()
        datadict['snowfeed'] = 1;
        datadict['miunowfeed']=1;
        datadict['MATnext'] = round(t5.out_db["MATnext"].find_record().level,2);
        datadict['MLnext'] = round(t5.out_db["MLnext"].find_record().level,2);
        datadict['Munext'] = round(t5.out_db["Munext"].find_record().level,2);
        datadict['TATMnext'] = round(t5.out_db["TATMnext"].find_record().level,2);
        datadict['TOCEANnext'] = round(t5.out_db["TOCEANnext"].find_record().level,2);
        datadict['CCAnext'] = round(t5.out_db["CCAnext"].find_record().level,2);
        datadict['Knext'] = round(t5.out_db["Knext"].find_record().level,2);
        print("Scenario bmult=" + str(iteration) + ":")
#        print("  Modelstatus: " + str(t5.out_db["ms"].find_record().value))
#        print("  Solvestatus: " + str(t5.out_db["ss"].find_record().value))
        print("  Obj: " + str(t5.out_db["dummy"].find_record().level))
        print("  Enow: " + str(t5.out_db["Enow"].find_record().level))
#        import pdb;pdb.set_trace();
##    endtime = datetime.datetime.now()
#    print ((endtime - starttime))



