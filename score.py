# def score(card_combination)
#
# description:
#   evaluates the value of a combination of 5 cards (5card Hold'em rules)
#
# arguments:
#   card_combination... a list of 5 cards, each represented as a string, e.g. ['Ac', '3d', 'Th', '7h', 'Tc']
#
# return:
#   the value of the card_combination as an integer (as a 6digit hex string). The better the cards, the higher the value.
#
# details:
#   At first, we count the number of appearances of the ranks and colors indivdually.
#   Next, we sort the ranks by the number of their appearence in descending order.
#   If the number of appearances of some cards is equal, they will be sorted in descending order by their rank_value (=> AK8K8 will be sorted to K8A)
#   Depending on the amount of appearences of the different ranks we now can assign the first digit of the resulting hex number, which represents the strength of the hand
#   '0x9' straight flush(**), '0x7' 4 of a kind, '0x6' full house, '0x5' flush, '0x4' straight, '0x3' 3 of a kind, '0x2' 2pair, '0x1' 1pair, '0x0' high card   (**): straight flush could also be '0x8', but since 4(straight) + 5(flush) = 9, it's '0x9'
#   This way, a straight will always have a higher value than a 2pair. We only need to check for a flush or a straight, if every rank appears only once. 
#   The last 5 digits represent the ranks sorted by appearance and value in descending order. This way e.g. a 2pair QQ55K ->'0x2aa33b' will be higher than QQ55T -> '0x2aa338'

card_values = {'2':0, '3':1, '4':2, '5':3, '6':4, '7':5, '8':6, '9':7, 'T':8, 'J':9, 'Q':10, 'K':11, 'A':12}

def score(card_combination):
  global card_values
  
  ranks = {}
  colors = {'h':0, 'd':0, 's': 0, 'c':0}
  for card in card_combination:
    colors[card[1]] += 1     # count the colors
    if card[0] in ranks:     # count the ranks
      ranks[card[0]] += 1
    else:
      ranks[card[0]] = 1

  sorted_ranks = sorted(ranks.keys(), key=lambda x:(-ranks[x],-card_values[x]))   # ['7c', 'Ad', 'Th', '7h', 'Tc'] --> ['T', '7', 'A']  (access the amount of appearances of 'T' via ranks['T'] )
  max_count = ranks[sorted_ranks[0]]
  if max_count == 4:
    hand_value = '0x7'
  elif max_count == 3:
    hand_value = '0x' + str(3*ranks[sorted_ranks[1]])   # '0x6' for a fullhouse, '0x3' for 3 of a kind
  elif max_count == 2:
    hand_value = '0x' + str(ranks[sorted_ranks[1]])     # '0x2' for 2pair, '0x1' for 1pair
  else:  # every rank appears only once. Either a flush or a straight (or both) or nothing but a high card
    flush = max(colors.values()) == 5     # check for flush
    straight = 0                          # check for straight:
    if (card_values[sorted_ranks[0]] - card_values[sorted_ranks[4]]) == 4:  # difference between highest and lowest card in a straight is 4
      straight = 1
    elif (sorted_ranks[0] == 'A' and sorted_ranks[1] == '5'):   # check for a wheel (5,4,3,2,A)
      straight = 1
      sorted_ranks.pop(0)         # get rid of the 'A' at the beginning, since '5' is the highest card in a wheel
      sorted_ranks.append('2')    # append anything to receive a 6 digit hex code in the end, it doesn't really matter what we append here. Can you hear the catchy tune? :)
    hand_value = '0x' + str(5*flush + 4*straight)  # '0x9' for a straight flush, '0x5' for aflush, '0x4' for a straight, '0x0' for a high card
  for r in sorted_ranks:          # assign the other 5 digits 
    hand_value += ranks[r]*hex(card_values[r])[2]
  return(hand_value)




# def eval_multiple(hands)
#
# description:
#   checks the value of multiple hands and sorts them by value in descending order
#
# arguments:
#   hands... a list of hands. Each hand consists of a list of 5 cards, represented as a string, e.g. [['8c', 'Ts', 'Kc', '9h', '4s'], ['7d', '2s', '5d', '3s', 'Ac']]

def eval_multiple(hands):
  scores = sorted([[i,score(hand)] for i, hand in enumerate(hands)], key=lambda x:-int(x[1],16))
  #if (scores[0][1] == scores[1][1]):
  #  print("Unentschieden")
  #else:
  #  print('Die beste Hand ist ' + ' '.join(hands[max(scores, key=lambda x:x[1])[0]]))   ## max scores kann raus, da scores ja bereits sortiert ist .join(hands[scores[0][0]])

    
if __name__ == '__main__':
  import timeit
  print(timeit.timeit("eval_multiple([['8c', 'Ts', 'Kc', '9h', '4s'], ['7d', '2s', '5d', '3s', 'Ac'], ['8c', 'Ad', '8d', 'Ac', '9c'], ['7c', '5h', '8d', 'Td', 'Ks']])", number=1000000, setup="from __main__ import eval_multiple, score"))
  #eval_multiple([['Tc','8c','Jc','7c','9c'],['4c','3c','Ac','5c','2c'],['8c','8s','8d','9d','8h'],['Qc','7s','Qd','7d','7h'],['Tc','8c','Jc','2c','9c'],['Tc','8c','Jc','7h','9d'],['4d','3c','Ac','5h','2c'],['Tc','Ks','3d','Kd','Kc'],['7c','Kc','4h','7d','Kc'],['7d','8s','Qs','8c','4c'],['Kc','As','3d','7d','Tc'],['2c','3s','4d','5d','6c'],['Ac','Ks','Qd','Jd','Tc']])
  eval_multiple([['Tc','8c','Jc','7c','9c'],['4c','3c','Ac','5c','2c'],['8c','8s','8d','9d','8h'],['Qc','7s','Qd','7d','7h'],['Tc','8c','Jc','2c','9c'],['Tc','8c','Jc','7h','9d'],['4d','3c','Ac','5h','2c'],['Tc','Ks','3d','Kd','Kc'],['7c','Kc','4h','7d','Kc'],['7d','8s','Qs','8c','4c'],['Kc','As','3d','7d','Tc'],['2c','3s','4d','5d','6c'],['Ac','Ks','Qd','Jd','Tc']])
  eval_multiple([['Qc','Tc','9h','Jd','Kd'], ['Qd','Jd','9d','Th','Kd'],['Th','8h','3h','2h','7h'],['7d','8s','Qs','8c','4c'],['Th','8h','4h','2h','7h']])
  eval_multiple([['Td','8s','Qs','8c','4c'], ['7c','2c','Qh','7d','Kc'], ['Tc','8c','5c','8h','Qd']])
  #score(['Tc','8c','Jc','7c','9c']) #straight flush
  #score(['4c','3c','Ac','5c','2c']) #straight flush 5 high
  #score(['8c','8s','8d','Td','8h']) #4 of a kind
  #score(['Qc','7s','Qd','7d','7h']) #fullhouse
  #score(['Tc','8c','Jc','2c','9c']) #flush
  #score(['Tc','8c','Jc','7h','9d']) #straight
  #score(['4d','3c','Ac','5h','2c']) #straight 5 high
  #score(['Kc','Ks','Ad','Kd','Tc']) #3 of a kind
  #score(['7c','Kc','4h','7d','Kc']) #2pair
  #score(['7d','8s','Qs','8c','4c']) #1pair
  #score(['Kc','As','3d','7d','Tc']) #high card
  #score(['2c','3s','4d','5d','6c']) #straight
  #score(['Ac','Ks','Qd','Jd','Tc']) #straight