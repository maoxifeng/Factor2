# -*- coding: utf-8 -*-

##mod2.py
#import mod1 as md 
#
#md.main()
#
#print __name__


# same result as above
def mod2_main():

    a = 3
    print 'a: %s' %a
    import mod1 
    print 'mod1.main:',
    mod1.main()
    print __name__
print 'aa'
print __name__
mod2_main()

if __name__ == '__main__':
    print '\nrun mod2_main again'
    mod2_main()
