from flask import Flask,request
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate,identity


app= Flask(__name__)
app.secret_key='saif'
api=Api(app)

jwt= JWT(app,authenticate,identity) #/auth
items=[]
class Item_List(Resource):
    def get(self):
        return {'item':items}
class Item(Resource):
    @jwt_required()
    def get(self,name):
        # for i in items:
        #     if i['name']==name:
        #
        #         return i
        item=next(filter(lambda x:x['name']==name,items),None)
        return {'item':item},200 if item else 404

    def post(self, name):

        if next(filter(lambda x:x['name']==name,items),None):
            return {'Message ': 'Items Already Exsist'},400
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items=list(filter(lambda x:x['name']!=name,items))  #making list of items which does not include the item we want to delete
        return {'message':'Item Deleted Successfully'}


    def put(self,name):
        parser=reqparse.RequestParser()
        parser.add_argument('price',type=float,required=True,help='This fileld cannot be left blank')
        #data = request.get_json()  #if we use parser it would only update the items which are inculded in parser argument
        data=parser.parse_args()

        item=next(filter(lambda x:x['name']==name,items),None)
        if item is None:
            item={'name':name,'price':data['price']}
            items.append(item)
            return item
        else:
            item.update(data)
        return item







    # def post(self, name):
    #     data=request.get_json()
    #     item={'name':name,'price':data['price']}
    #     items.append(item)
    #     return item,201

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Item_List, '/item/')

app.run(port=4999,debug=True)