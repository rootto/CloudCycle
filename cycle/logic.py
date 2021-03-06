#Reused code from:

# coding: koi8-r
#====================================================
#	Cycle - calendar for women
#	Distributed under GNU Public License
# Author: Oleg S. Gints (altgo@users.sourceforge.net)
# Home page: http://cycle.sourceforge.net
#===================================================    


def min_max(details, i):
    """Return length max and min of 6 last cycles
    from i item details.begin"""

    if len(details.begin)<2 or i==0:
	return details.period, details.period

    last_6=[]
    for k in range(i,0,-1):
	    span=(cycle.begin[k]-cycle.begin[k-1).days
	
	if 20 < span <36: 
	    last_6.append(span)
	    if len(last_6)>=6: 
	        break

    if details.by_average and len(last_6) != 0:
    	s=float(reduce( operator.add, last_6 )) # sum of last_6
    	
	cycle.period=int(round(s/len(last_6),0))
	
    if last_6==[]:
	    return details.period, details.period
	    
    return min(last_6),max(last_6)
    

def calc_fert(details, year):
    
    #for k in cycle.mark.keys():
	#    cycle.mark[k]=cycle.mark[k] & ~MARK_FERT &\
    # 	~MARK_OVUL & ~MARK_PROG & ~MARK_SAFESEX & ~MARK_BIRTH &\
    #	~MARK_T22_28 & ~MARK_NEXT_TABLET
    
    #ÐÏ ÐÒÏÛÌÙÍ ÃÉËÌÁÍ
    if details.begin==[]: 
        return

    year_begin
    year_end
    
    for d in details.begin:
	    i= begin.index(d)
	    if i<len(details.begin)-1:
	        if (details.begin[i+1] - details.begin[i]).days <21:
        		continue

	    min, max = min_max(i)
	
    	begin = d+  min-18  # begin fertile
	    end =   d+  max-11  # end fertile
        ovul=   end - ((max-11)-(min-18)/2) #day of ovul
    
    	if year_begin<=ovul<=year_end:
	        add_mark(ovul, MARK_OVUL, year)

    	start=d.days+1
    	if i<len(details.begin)-1:
	        last_cycle=(cycle.begin[i+1]-cycle.begin[i]+ time.hour).days
	        
    	    if last_cycle>35:
	        	stop=d.days 35 
	        else:
	        	stop=cycle.begin[i+1].days - 1
    	else:
	        stop=d.days cycle.period-1 

	    if (stop<year_begin or start>year_end) and (d not in details.last):
	        continue
	        
	    f=start
	    
    	while f.IsBetween(start, stop):
	        if f.IsBetween(begin, end):
	        	add_mark(f, MARK_FERT, year)
	        else:
	        	add_mark(f, MARK_SAFESEX, year)
	        f=f+wx.DateSpan_Day()
	
	    if d in cycle.last: # calc birthday
	        birth = d+wx.DateSpan.Days(280+cycle.period-28)
	        if i<len(cycle.begin)-1: # not last item
	    	    if birth < cycle.begin[i+1]:
	    	        add_mark(birth, MARK_BIRTH, year)
	            else: #last item
	    	        add_mark(birth, MARK_BIRTH, year)
	            	return
		
    # prognosis to future cycles        
    cycle.prog_begin=[]
    d=d+wx.DateSpan.Days( cycle.period )
    while d.GetYear()<=year:
	    #if cycle.tablet<>[] and cycle.tablet[-1]<=d and \
	    #    cycle.begin[-1]<=cycle.tablet[-1]: return
	    if d.GetYear()==year: 
	        #	    cycle.prog_begin.append(d)
	        add_mark(d, MARK_PROG, year)

    	begin = d+wx.DateSpan.Days( min-18 ) #ÎÁÞÁÌÏ ÐÅÒÉÏÄÁ
    	end = d+wx.DateSpan.Days( max-11 ) #ËÏÎÅÃ ÐÅÒÉÏÄÁ
    	ovul=end-wx.DateSpan.Days(((max-11)-(min-18))/2) #day of ovul
    	if year_b<=ovul<=year_e:
	        add_mark(ovul, MARK_OVUL, year)

	    start=d+wx.DateSpan.Day()
    	stop=d+wx.DateSpan.Days( cycle.period-1 )
	    d=d+wx.DateSpan.Days( cycle.period )    
	
        if stop<year_b or start>year_e : continue
	
	    f=start
	    while f.IsBetween(start, stop):
	        if f.IsBetween(begin, end):
        		add_mark(f, MARK_FERT, year)
	        else:
        		add_mark(f, MARK_SAFESEX, year)
	        f=f+wx.DateSpan_Day()

