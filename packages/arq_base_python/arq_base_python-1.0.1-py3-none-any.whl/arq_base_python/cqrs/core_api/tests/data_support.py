class DataSupport:
    command_names = ["task.save"]
    not_indicated_channel_message = "CANAL_NO_INDICADO"
    identification_types = ["CC", "PS"]
    default_task_name = "task1"
    default_description = "Task created from Python micro"
    default_tags = [
        {
            "name": "demo"
        },
        {
            "name": "architecture"
        }
    ]