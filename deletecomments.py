def deletecomments(comment_id, user_id):
    for comment in comments_db:
        if comment["comment_id"] == comment_id:
            if comment["user_id"] == user_id:
                comments_db.remove(comment)
                return {"status": "success", "message": "Comment deleted successfully."}
            else:
                return {"status": "error", "message": "Unauthorized: You can only delete your own comments."}

    return {"status": "error", "message": "Comment not found."}

# Example usage for delete_comment
response = delete_comment(comment_id=1, user_id=101)
print(response)