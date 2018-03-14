# -*-coding:utf-8-*-
import pymysql
import redis
import pymongo
import traceback
from my_logging import MyLogger

# 将数据从mysql中取出
def get_mysql_data():
	try:
		params = {
					'host':'',
					'port':3306,
					'database':'',
					'user':'',
					'password':'',
					'charset':'utf8'
				}
		conn = pymysql.connect(**params)
		cur = conn.cursor()
		sql = 'select id, name, id_card from t_bank_card where state=1 group by id_no'
		cur.execute(sql)
		data = cur.fetchall()
		return data
	except:
		# todo 记录日志
		print traceback.format_exc()
	finally:
		cur.close()
		conn.close()

# 将数据存入redis(使用redis作为中间缓存, 分为两张表， 一张是待爬取的表， 一张是已经爬取的表)
class RedisHandler():
	def __init__(self):
		self._redis = redis.Redis()
		self.logger = MyLogger('redis_handler')

	# 将mysql的数据存入待爬表(data应是由上面的get_mysql_data函数运行获取的结果)
	def save_to_prepare(self, data):
		try:
			data = map(lambda x:(str(x[0]), x[1], x[2]), data)
			for each in data:
				print each[0]
				self._redis.sadd('PREPARE_QUEUE', '|'.join(each))
		except:
			self.logger.warning(traceback.format_exc())

	# 从待爬表取出num条数据
	def get_from_prepare(self):
		try:
			data = self._redis.spop('PREPARE_QUEUE')
			if data:
				return data.split('|')
		except:
			self.logger.warning(traceback.format_exc())

	# 将数据存入已爬表
	def save_to_completed(self, data):
		try:
			self._redis.sadd('COMPLETED_QUEUE', data)
		except:
			self.logger.warning(traceback.format_exc())

	# 检查数据是否在已爬表中
	def check_completed(self, data):
		return self._redis.sismember('COMPLETED_QUEUE', data)


# 将结果存入mongodb
class MongoHandler():
	def __init__(self):
		self._mongo = pymongo.MongoClient()
		self.logger = MyLogger('mongo_handler')

	def save_data(self, data):
		try:
			self._mongo.db.bjh_data.update(
				{
					'customer_id':data['customer_id'],
					'id_card':data['id_card'],
					'name':data['name']
					},
				{'$set':data}, True, True)
		except:
			self.logger.warning(traceback.format_exc())


if __name__ == '__main__':
	data = get_mysql_data()
	print data
