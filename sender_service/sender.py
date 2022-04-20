"""Осуществляет получение сообщений и получателй от API и отправляет на API внешнего сервиса отправки"""
import datetime

import pika
import requests

from sender_service.variables import PIKA_HOST, API_HOST, TOKEN

delay_list = []
message_list = []


def request_replay(message_id):
    """
    Сообщает API о необходимости повторной попытке отправки
    :param message_id: id сообщения
    :return: None
    """
    return requests.patch(url=f'{API_HOST}api/message/{message_id}', json={'sending_status': 'RP'})


def sender(message):
    """
    Осуществляет проверку и отправку сообщений, изменяет статус сообщений
    :param message: сообщение
    :return: None
    """
    msg_id = message['id']
    phone = message['client_phone']
    text = message['message']
    start_time = datetime.datetime.strptime(message['mail_start'], '%Y-%m-%dT%H:%M:%SZ')
    end_time = datetime.datetime.strptime(message['mail_end'], '%Y-%m-%dT%H:%M:%SZ')

    headers = {
        'Authorization': f'Bearer {TOKEN}',
    }
    data = {
        'id': msg_id,
        'phone': phone,
        'text': text
    }

    if start_time <= datetime.datetime.now() <= end_time:
        try:
            response = requests.post(f'https://probe.fbrq.cloud/v1/send/{msg_id}',
                                     headers=headers, json=data, timeout=2)
        except requests.exceptions.HTTPError as err:
            print(f'HTTPerror: {err}')
            resp = request_replay(msg_id)
        except Exception as err:
            print(f'Other error: {err}')
            resp = request_replay(msg_id)
        else:
            if response.status_code == 200:
                requests.patch(url=f'{API_HOST}api/message/{msg_id}', json={'sending_status': 'CP'})
                print('completed')
            else:
                resp = request_replay(msg_id)
                print('repeated')
    elif start_time > datetime.datetime.now():
        requests.patch(url=f'{API_HOST}api/message/{msg_id}', json={'sending_status': 'DL'})
        print('delay')
    else:
        requests.patch(url=f'{API_HOST}api/message/{msg_id}', json={'sending_status': 'ERR'})
        print('error')


# def callback(ch, method, properties, body):
def callback(body):
    msg_id = body
    msg = requests.get(url=f'{API_HOST}api/message/{msg_id}').json()
    sender(msg)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(PIKA_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='sending')
    channel.basic_consume(queue='sending', on_message_callback=callback)
    channel.start_consuming()


if __name__ == '__main__':
    callback(body=6)
