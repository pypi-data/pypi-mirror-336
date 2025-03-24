#================================================================================================
#libraries: 

from art import text2art
from snl_regression_quality.modules.utils.global_constants import GREEN, RED,BLUE,  RESET   
#================================================================================================


def initial_message():


    space_1 = '            '

    space_4 = '                           '
    # space_2 = '                  '
    # space_3 = '                     '
    # art_text1 = text2art(space_3+"SIMPLE") 
    # art_text11 = text2art(space_1+"NO   LINEAR") 
    # art_text2 = text2art(space_1+"REGRESION")  
    # art_text3 = text2art(space_2+"QUALITY")  
    # print('++++'*20)
    # print(art_text1)
    # print(art_text11)
    # print(art_text2)
    # print(art_text3)

    art_text4= text2art(space_4+"S.N.L.")
    art_text5 = text2art(space_1+"REGRESION")  
    

    print('++++'*20)
    print(art_text4)
    print(art_text5)
    
    print(BLUE+'===='*20+RESET)
    print(BLUE+'Part 1, Assumption calculation: '+RESET)
    print(BLUE+'===='*20+RESET)