class Group(object):
    def __init__(self, _name):
        self.name = _name
        self.groups = []
        self.users = []

    def add_group(self, group):
        self.groups.append(group)

    def add_user(self, user):
        self.users.append(user)

    def get_groups(self):
        return self.groups

    def get_users(self):
        return self.users

    def get_name(self):
        return self.name

    def is_user_in_group(user, group):
        """
        Return True if user is in the group, False otherwise.

        Args:
          user(str): user name/id
          group(class:Group): group to check user membership against
        """
        if not group:
            return

        visited = dict()

        def is_user_in_group_recursive(user, group, visited):
            # base case
            if user in group.get_users():
                return True

            for grp in group.get_groups():
                group_name = grp.get_name()
                flag = False
                if not visited.get(group_name):
                    flag = is_user_in_group_recursive(user, grp, visited)
                    visited[group_name] = True

                if flag:
                    return True

            return False

        return is_user_in_group_recursive(user, group, visited)


parent = Group("parent")
child = Group("child")
evil_child = Group("evil_child")
sub_child = Group("subchild")
evil_sub_child = Group("evil_sub_child")

sub_child_user = "sub_child_user"
sub_child.add_user(sub_child_user)

child.add_group(sub_child)
evil_child.add_group(evil_sub_child)
parent.add_group(child)
parent.add_group(evil_child)

# Test case 1

print(Group.is_user_in_group("sub_child_user", parent))
# expected: True

# Test case 2

print(Group.is_user_in_group("fake", parent))
# expected: False

# Test case 3

print(Group.is_user_in_group("sub_child_user", None))
# expected: None

# Test case 4

print(Group.is_user_in_group("", parent))
# expected: False
