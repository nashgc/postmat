"""
Simple postmat manager, get ids from args then create objects and get their status and work_now
"""


from postmat import Postmat
import argparse

parser = argparse.ArgumentParser(description='Postmat manager')
parser.add_argument('--num', dest='nums',  nargs='+', type=int, help='enter numbers of postmat space separated: --num 100 101 102')

args = parser.parse_args()
parser.print_help()
postmats_obj = []
if args.nums != None:
    for num in args.nums:
        postmats_obj.append(Postmat(num))
    for obj in postmats_obj:
        if obj.status == None:
            print('Postmat #{} Не найден'.format(obj.postmat_id))
        else:
            print('Postmat #{} | Статус: {} | Работает сейчас: {}'.format(obj.postmat_id, obj.status, obj.work_today))
else:
    parser.print_help()
