def find_user(data, username):
  for user in data["users"]:
    if (user["username"] == username):
      return user
  return None


def find_event(data, name):
  for event in data["events"]:
    if (event["name"] == name):
      return event
  return None
