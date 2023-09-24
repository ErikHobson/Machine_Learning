### SOFT SENSOR D50 ###
'''
This module is the solf sensor for D50C on the grinding mill circuit. Functions defined as a function of ore feed are Interior:
cyc_vol
rho
lumda

Function of feed and Pressure: (feed, P) 

D50_4_CL
unit_cyc
numcyc

Function of feed and Pressure and cyc_vol: (cyc_vol, feed, P)

D50_from_vol

This function uses measured cyc_volume measurement instead of assuming circulating load of 400.

'''

feed_0=110.0  #input:feed
P_0= 75.8  #input: cyclone pressure

sg=2.6
#circ_L=4.000 #400% circulating load       #we now have direct measurement of flow rate. take out
feed_p=0.605  #60 %S Cyclone feed
rho=1.61

DC =0.381 #m     Cyclone diameter
DI =0.152 #m     Inner diameter
DO=0.17145 #m    Vortex finder diameter
DU=0.1016 #m     Spigot diameter
LC   =0.641 #m   cyclone length
theta =15 #deg   cone angle
KD0   =6.00e-5  #D50 constant
KQ0   =490       #capacity const
KV1   =6.6       #volume split constant
KW1   =8.4       #water split conts
alpha =3.9       #eff curve sharpness
beta  =0.0       #init dip in eff


# def circ_Load(flowrate ,feed ):
    
#     return





circ_L=4.000

def D50_4_CL(feed,P):
    circ_L=4.000
    
    def cyc_vol(feed):
        a=feed*(1+circ_L)/feed_p
        b=feed*(1+circ_L)
        c=feed*(1+circ_L)/sg
        cvol=a-b+c
        return cvol

    def rho(feed):
        cvol=cyc_vol(feed)
        a=feed*(1+circ_L)/feed_p
        b=feed*(1+circ_L)
        c=feed*(1+circ_L)/sg
        d= a/ (a - b +c)
        return d

    def lumda(feed):
        c=feed*(1+circ_L)/sg   #replace  feed*(1+circ_L)   with flow rate
        l= 10**((1.82*c)/(cyc_vol(feed))) / (8.05*(1-c/cyc_vol(feed))**2)
        return l

    f1= DC*KD0* (DC**(-0.65)) *((DO/DC)**0.52) *((DU/DC)**(-0.47)) *((DI/DC)**(-0.5)) \
    *((LC/DC)**0.2) *(theta**0.15) *((P/(rho(feed)*9.8*DC))**(-0.22)) *(lumda(feed)**0.93)
    
    return f1*1000



def unit_cap(feed,P):
    return KQ0*DC**(-0.1)*(DO/DC)**0.68 *(DI/DC)**0.45 *(LC/DC)**0.2 *theta**-0.1 *DC**2 *(P/rho(feed))**0.5 

def numcyc(feed,P):
    return cyc_vol/unit_cap(feed,P)




def D50_meas_vol(cyc_vol,feed, P_):    #from measured volume
    
    P=P_*6.0
    
    OF=feed*1.0
    sl_dens= 100 / (100*feed_p/sg + (100-feed_p*100))
    cyc_feed=cyc_vol *feed_p *sl_dens
    UF=cyc_feed-OF
    circ_L=UF/OF
    
    def rho(feed):
        cvol=cyc_vol*1.0
        a=feed*(1+circ_L)/feed_p
        b=feed*(1+circ_L)
        c=feed*(1+circ_L)/sg
        d= a/ (a - b +c)
        return d

    def lumda(feed):
        c=feed*(1+circ_L)/sg   #replace  feed*(1+circ_L)   with flow rate
        l= 10**((1.82*c)/(cyc_vol)) / (8.05*(1-c/cyc_vol)**2)
        return l

    def D50_4_CL(feed,P):
        f1= DC*KD0* (DC**(-0.65)) *((DO/DC)**0.52) *((DU/DC)**(-0.47)) *((DI/DC)**(-0.5)) \
        *((LC/DC)**0.2) *(theta**0.15) *((P/(rho(feed)*9.8*DC))**(-0.22)) *(lumda(feed)**0.93)
        return f1*1000
    
    return  D50_4_CL(feed,P)   #, rho(feed), lumda(feed), sl_dens, circ_L
    


#WHAT is the time constant? Do feed changes affect D50 immediately?
