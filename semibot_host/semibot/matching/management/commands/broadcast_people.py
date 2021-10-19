from django.core.management.base import BaseCommand
import matching.matching as matching
import matching.grpc_client as grpc_client

class Command(BaseCommand):
    help = """Send message to data_manager's people
    """

    def handle(self, *args, **options):
        personal_data = grpc_client.get_personal_data_dict()

        for person in personal_data.values():
            msg = '学籍番号(ID): ' + person.id + '\n'
            msg += '名前: ' + person.name + '\n'
            msg += 'ラベル: '
            for label in person.labels:
                msg += label + '\n'

            matching.send_message(person.message_addr, msg)

