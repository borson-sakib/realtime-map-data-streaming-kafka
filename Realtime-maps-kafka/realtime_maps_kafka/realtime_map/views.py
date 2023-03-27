from django.shortcuts import render

from pykafka import KafkaClient
import json
from datetime import datetime
import uuid
from django.http import HttpResponse, JsonResponse


# Create your views here.

def generate_uuid():
    return uuid.uuid4()

def data_pass(request):
    if request.method == 'POST':
        client = KafkaClient(hosts="localhost:9092")
    
        topic = client.topics['new-topic']
        producer = topic.get_sync_producer()
        
        message = request.POST['my_data']
        print(message)
        producer.produce(message.encode('ascii'))
    return render(request, 'index.html')
        

def index(request):
    client = KafkaClient(hosts="localhost:9092")
    
    topic = client.topics['new-topic']
    producer = topic.get_sync_producer()
    

    
    input_file = open('./static/data/locations.json')
    json_arr = json.load(input_file)
    
    coordinates = json_arr['features'][0]['geometry']['coordinates']
    corrs = json_arr['features'][0]['geometry']['coordinates']
    
    # message = (str()).encode('ascii')
    # producer.produce(message)
    data = {}
    data['busline']= '001'
    def generate_checkpoint (coordinates):
        i=0

        while i < len (coordinates) :
            data['key'] = data['busline'] + "." + str(generate_uuid())
            data['timestamp' ] = str(datetime.utcnow())
            data['latitude'] = coordinates[i][1]
            data[ 'longitude'] = coordinates[i][0]
            message = json.dumps (data)
            print (message)
            producer.produce (message. encode('ascii'))

        #if bus reaches last coordinate, start from beginning
            if i == len(coordinates) -1:
                i=0
            else:
                i+=1
    
    # generate_checkpoint (coordinates)
    
    
    # for i in corrs:
    #     message= str(i).encode('ascii')
    #     producer.produce(message)

    print(client.topics)
    # print(json_arr['features'])
    
    return render(request,'index.html')

def get_messages(request):
    client = KafkaClient(hosts="localhost:9092")
    def events():
        for i in client.topics['test_kafka_map'].get_simple_consumer():
            yield 'data:{0}\n\n'.format(i.value.decode())
    return HttpResponse(events(), mimetype="text/event-stream")

from django.http import StreamingHttpResponse
import time

def stream(request):
    client = KafkaClient(hosts="localhost:9092")

    def event_stream():
        for i in client.topics['new-topic'].get_simple_consumer():
            yield 'data:{0}\n\n'.format(i.value.decode())
            # time.sleep(1)

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response

# from pykafka import ClusterMetadata
# from pykafka.exceptions import TopicAlreadyExistsError, LeaderNotAvailable
from kafka.admin import KafkaAdminClient, NewTopic


def delete_message(request):
    try:
        # client = KafkaClient(hosts="localhost:9092")

        # # Set up topic object
        # topic = client.topics[b"test_kafka_map"]
        
        # # Delete existing topic
        # client.delete_topics(["test_kafka_map"])

        # # Set up metadata object
        # metadata = ClusterMetadata(client)

        # # Create new topic
        # metadata.add_topic("new-topic")
        
        # Set up Kafka admin client
        admin_client = KafkaAdminClient(bootstrap_servers="localhost:9092")

        # Create new topic
        # new_topic = NewTopic(name="new-topic", num_partitions=1, replication_factor=1)
        # admin_client.create_topics([new_topic])
        
        delete_request = DeleteTopicsRequest(["test_kafka_map"])
        admin_client.delete_topics(delete_request)
        return HttpResponse('successful')
    
    except Exception as e:
        return HttpResponse(str(e))