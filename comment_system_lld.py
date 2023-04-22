from typing import List

class Comment:
    def __init__(self, description: str):
        self.id = self.get_unique_comment_id()
        self.parent_id = ''
        self.user_id = ''
        self.post_id = ''
        self.description = description
        self.comments = []

    def get_comments(self) -> List['Comment']:
        return self.comments

    def get_description(self) -> str:
        return self.description

    def set_description(self, description: str) -> None:
        self.description = description

    def get_id(self) -> str:
        return self.id

    def get_parent_id(self) -> str:
        return self.parent_id

    def set_parent_id(self, parent_id: str) -> None:
        self.parent_id = parent_id

    def get_post_id(self) -> str:
        return self.post_id

    def set_post_id(self, post_id: str) -> None:
        self.post_id = post_id

    def get_user_id(self) -> str:
        return self.user_id

    def set_user_id(self, user_id: str) -> None:
        self.user_id = user_id

    def add_comment(self, comment: 'Comment') -> None:
        self.comments.append(comment)

    def set_nested_description(self, comment_id: str, description: str) -> None:
        for comment in self.comments:
            if comment.id == comment_id:
                comment.set_description(description)
                return

    def set_nested_delete(self, comment_id: str) -> None:
        i = 0
        for comment in self.comments:
            if comment.id == comment_id:
                self.comments.pop(i)
                return
            i += 1

    @staticmethod
    def get_unique_comment_id() -> str:
        Comment.comment_id = Comment.comment_id + 1 if hasattr(Comment, 'comment_id') else 1
        return 'c' + str(Comment.comment_id)

class Post:
    def __init__(self):
        self.id = self.get_unique_post_id()
        self.comments = []

    def get_comments(self) -> List[Comment]:
        return self.comments

    def get_id(self) -> str:
        return self.id

    def add_comment(self, comment: Comment) -> None:
        self.comments.append(comment)

    def add_nested_comment(self, comment_id: str, comment: Comment) -> None:
        for comm in self.comments:
            if comm.get_id() == comment_id:
                comm.add_comment(comment)
                return

    def edit_comment(self, parent_id: str, comment_id: str, description: str) -> None:
        for comment in self.comments:
            if comment.get_id() == parent_id:
                if parent_id == comment_id:
                    comment.set_description(description)
                else:
                    comment.set_nested_description(comment_id, description)
                break

    def delete_comment(self, parent_id: str, comment_id: str) -> None:
        i = 0
        index = -1
        for comment in self.comments:
            if comment.get_id() == parent_id:
                if parent_id == comment_id:
                    index = i
                    break
                else:
                    comment.set_nested_delete(comment_id)
                    return
            i += 1
        if index != -1:
            self.comments.pop(index)

    @staticmethod
    def get_unique_post_id() -> str:
        Post.post_id = Post.post_id + 1 if hasattr(Post, 'post_id') else 1
        return 'p' + str(Post.post_id)

class User:
    def __init__(self, name):
        self.name = name
        self.id = self.get_unique_user_id()

    @staticmethod
    def get_unique_user_id():
        User.user_id = getattr(User, 'user_id', 1)
        user_id = User.user_id
        User.user_id += 1
        return f"u{user_id}"

    def add_comment_to_post(self, post, comment):
        comment.set_user_id(self.id)
        comment.set_post_id(post.get_id())
        comment.set_parent_id(comment.get_id())
        post.add_comment(comment)

    def reply_to_comment(self, post, parent_id, comment):
        comment.set_user_id(self.id)
        comment.set_post_id(post.get_id())
        comment.set_parent_id(parent_id)
        post.add_nested_comment(parent_id, comment)

    def edit_comment(self, post, parent_id, comment_id, description):
        for comment in post.get_comments():
            if comment.get_id() == comment_id:
                if comment.get_user_id() != self.id:
                    print("Unauthorized to edit comment!")
                    return False
                break
        post.edit_comment(parent_id, comment_id, description)
        return True

    def delete_comment(self, post, parent_id, comment_id):
        for comment in post.get_comments():
            if comment.get_id() == comment_id:
                if comment.get_user_id() != self.id:
                    print("Unauthorized to delete comment!")
                    return False
                break
        post.delete_comment(parent_id, comment_id)
        return True

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name
        
if __name__ == '__main__':
    u1 = User("L")
    c1 = Comment("First Comment")
    c2 = Comment("Second Comment")
    c22 = Comment("Second nested comment")
    c11 = Comment("First nested comment")
    c12 = Comment("First Second nested comment")
    c13 = Comment("First Third nested comment")

    p = Post()
    u1.add_comment_to_post(p, c1)
    u1.add_comment_to_post(p, c2)
    u1.reply_to_comment(p, c1.get_id(), c11)
    u1.reply_to_comment(p, c1.get_id(), c12)
    u1.reply_to_comment(p, c1.get_id(), c13)
    u1.reply_to_comment(p, c2.get_id(), c22)

    for c in p.get_comments():
        print(c.get_description())
        for cmt in c.get_comments():
            print("\t", cmt.get_description())

    print("***********************************************************************")

    s12 = "1st 2nd comment"
    s11 = "1st 1st comment"

    u1.edit_comment(p, c1.get_id(), c11.get_id(), s11)

    for c in p.get_comments():
        print(c.get_description())
        for cmt in c.get_comments():
            print("\t", cmt.get_description())

    print("***********************************************************************")

    u1.delete_comment(p, c1.get_id(), c12.get_id())
    for c in p.get_comments():
        print(c.get_description())
        for cmt in c.get_comments():
            print("\t", cmt.get_description())

    print("***********************************************************************")

    u1.delete_comment(p, c1.get_id(), c1.get_id())
    for c in p.get_comments():
        print(c.get_description())
        for cmt in c.get_comments():
            print("\t", cmt.get_description())
