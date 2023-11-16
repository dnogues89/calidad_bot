data = {
    "object": "whatsapp_business_account",
    "entry": [
        {
            "id": "159738167225852",
            "changes": [
                {
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {
                            "display_phone_number": "15551309883",
                            "phone_number_id": "173974499122607"
                        },
                        "contacts": [
                            {
                                "profile": {
                                    "name": "DN"
                                },
                                "wa_id": "5491166531292"
                            }
                        ],
                        "messages": [
                            {
                                "context": {
                                    "from": "15551309883",
                                    "id": "wamid.HBgNNTQ5MTE2NjUzMTI5MhUCABEYEjgwM0MyRkZDNDA2QjlDRDczOAA="
                                },
                                "from": "5491166531292",
                                "id": "wamid.HBgNNTQ5MTE2NjUzMTI5MhUCABIYFjNFQjA3NzY2QTQwRTc5REMzQTc0RTEA",
                                "timestamp": "1700070964",
                                "type": "button",
                                "button": {
                                    "payload": "Ir a la encuesta",
                                    "text": "Ir a la encuesta"
                                }
                            }
                        ]
                    },
                    "field": "messages"
                }
            ]
        }
    ]
}

print(data["entry"][0]['changes'][0]['value']['messages'][0]['button']['text'])