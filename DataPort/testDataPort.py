#!/usr/bin/env python
# -*- coding: euc-jp -*-



import sys
import OpenRTM_aist
import RTC
import time

mgr = OpenRTM_aist.Manager.init(sys.argv)
mgr.activateManager()
mgr.runManager(True)

d_in = RTC.TimedDouble(RTC.Time(0,0),0)
inIn = OpenRTM_aist.InPort("in", d_in)
prop = OpenRTM_aist.Properties()
inIn.init(prop)

port_obj = inIn._this()

orb = mgr.getORB()
rtc_name = "corbaname::localhost:2809/NameService#MyFirstComponent0.rtc"
rtc_obj = orb.string_to_object(rtc_name)
rtc = rtc_obj._narrow(RTC.RTObject)


#inIn.setOwner(rtc)


ports = rtc.get_ports()

for p in ports:
    profile = p.get_port_profile()
    port_name = profile.name.split('.')[1]
    if port_name == "out":
        #p.disconnect_all()
        conprof = RTC.ConnectorProfile("testtest", "", [port_obj,p], [])
        OpenRTM_aist.CORBA_SeqUtil.push_back(conprof.properties,
                OpenRTM_aist.NVUtil.newNV("dataport.interface_type","corba_cdr"))
        OpenRTM_aist.CORBA_SeqUtil.push_back(conprof.properties,
                OpenRTM_aist.NVUtil.newNV("dataport.dataflow_type","push"))
        OpenRTM_aist.CORBA_SeqUtil.push_back(conprof.properties,
                OpenRTM_aist.NVUtil.newNV("dataport.subscription_type","Flush"))
        ret = p.connect(conprof)
        #print ret

while True:
    if inIn.isNew():
        data = inIn.read()
        print data.data
    time.sleep(0.1)