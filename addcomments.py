# Mock database (rto be replaced by Merna )
comments_db = []

def addcomments(event_id, user_id, content):

    if not content.strip():
        return {"status": "error", "message": "Comment content cannot be empty."}

    comment_id = len(comments_db) + 1  # Simulating auto-increment

    new_comment = {
        "comment_id": comment_id,
        "event_id": event_id,
        "user_id": user_id,
        "content": content,
    }

    comments_db.append(new_comment)
    return {"status": "success", "message": "Comment added successfully.", "comment": new_comment}

# Example usage for add_comment
response = add_comment(event_id=1, user_id=101, content="This is a great event!")
print(response)
