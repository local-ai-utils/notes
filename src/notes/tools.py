from .main import insert_note, create_category, assign_category

config = {}
def set_config(conf):
    global config
    config = conf

def create(note_text, categories):
    try:
        # Be very defensive here, because it's a response coming back from AI
        if note_text and type(note_text) is str:
            note_id = insert_note(note_text)

            # Confirm categories is an array
            if type(categories) is list:
                for category in categories:
                    if type(category) is str:
                        category_id = create_category(category)
                        assign_category(note_id, category_id)
        else:
            return "Note text not provided to tool"
            
        return True
    except Exception as e:
        return str(e)