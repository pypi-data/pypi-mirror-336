import click
import requests
from cli.utils import load_api_key

API_URL = "http://localhost:8000/api/reddit"

@click.group()
def bbs():
    """🧵 CLI BBS System — Create and browse threads, communities, and comments."""
    pass


USER_LOOKUP_URL = "https://api.minakilabs.dev/api/social/user"  # or your internal API base

import textwrap

import textwrap
import click

def render_thread(thread):
    click.secho("═" * 60, fg="yellow")
    click.secho(f"🧵 THREAD: {thread.get('title', 'No Title')}", bold=True, fg="cyan")
    if "community_id" in thread:
        click.echo(f"📍 Community ID: {thread['community_id']}")
    click.echo(f"👤 User: {thread.get('user_id', 'unknown')}    🕒 {thread.get('timestamp', 'unknown')}")
    click.secho("─" * 60, fg="white")
    click.echo(textwrap.fill(thread.get('content', ''), width=60))
    click.secho("─" * 60, fg="white")
    click.echo(f"📎 Thread ID: {thread.get('id', '?')}")
    click.secho("═" * 60 + "\n", fg="yellow")

def render_comment(comment):
    click.secho("━" * 60, fg="green")
    click.echo(f"👤 {comment.get('user_id', 'unknown')}    🕒 {comment.get('timestamp', 'unknown')}")
    click.echo(textwrap.fill(comment.get('content', ''), width=60))
    click.secho("━" * 60, fg="green")

def render_threads_list(threads):
    for thread in threads:
        render_thread(thread)

def render_comments_list(comments):
    for comment in comments:
        render_comment(comment)

def get_user_id(username, api_key):
    """Retrieve user ID from username via API."""
    try:
        url = f"{USER_LOOKUP_URL}/{username}"
        response = requests.get(url, headers={"apikey": api_key})
        if response.status_code == 200:
            return response.json().get("user_id")
        elif response.status_code == 404:
            click.secho(f"❌ User '{username}' not found.", fg="red")
        else:
            click.secho(f"❌ API Error: {response.text}", fg="red")
    except requests.exceptions.RequestException as e:
        click.secho(f"❌ Connection error: {e}", fg="red")
    return None

# ✅ Create Community
@click.command("create-community")
@click.argument("name")
@click.argument("description")
def create_community(name, description):
    """Create a new community."""
    api_key = load_api_key()
    res = requests.post(f"{API_URL}/community", headers={"apikey": api_key}, json={
        "name": name, "description": description
    })
    click.echo(res.json())


# ✅ List All Communities
@click.command("list-communities")
def list_communities():
    """List all communities."""
    #res = requests.get(f"{API_URL}/communities")
    api_key = load_api_key()
    res = requests.get(f"{API_URL}/communities", headers={"apikey": api_key})
    click.echo(res.json())

# ✅ Create Thread
@click.command("create-thread")
@click.argument("community_id", type=int)
@click.argument("title")
@click.argument("content")
def create_thread(community_id, title, content):
    """Create a thread in a community."""
    api_key = load_api_key()
    res = requests.post(f"{API_URL}/thread", headers={"apikey": api_key}, json={
        "community_id": community_id,
        "title": title,
        "content": content
    })
    click.echo(res.json())

# ✅ Get Threads in a Community
@click.command("get-community-threads")
@click.argument("community_id", type=int)
def get_threads_by_community(community_id):
    """List threads in a specific community."""
    api_key = load_api_key()
    headers = {"apikey": api_key}
    res = requests.get(f"{API_URL}/community/{community_id}/threads", headers=headers)
#    click.echo(res.json())
    threads = res.json()
    if not threads:
        click.secho("📭 No threads found in this community.", fg="yellow")
        return

    for thread in threads:
        render_thread(thread)


# ✅ Create Comment
@click.command("comment")
@click.argument("thread_id", type=int)
@click.argument("content")
def comment(thread_id, content):
    """Comment on a thread."""
    api_key = load_api_key()
    res = requests.post(f"{API_URL}/comment", headers={"apikey": api_key}, json={
        "thread_id": thread_id,
        "content": content
    })
    click.echo(res.json())

# ✅ Get Comments on a Thread
@click.command("get-comments")
@click.argument("thread_id", type=int)
def get_comments(thread_id):
    """List comments in a thread."""
    api_key = load_api_key()
    headers = {"apikey": api_key}
    res = requests.get(f"{API_URL}/thread/{thread_id}/comments", headers=headers)
    click.echo(res.json())


# ✅ Vote on Thread
@click.command("vote")
@click.argument("thread_id", type=int)
@click.argument("vote_type", type=click.Choice(["upvote", "downvote"]))
def vote(thread_id, vote_type):
    """Vote on a thread."""
    api_key = load_api_key()
    res = requests.post(f"{API_URL}/vote", headers={"apikey": api_key}, json={
        "thread_id": thread_id,
        "vote_type": vote_type
    })
    click.echo(res.json())

# ✅ Remove Vote
@click.command("remove-vote")
@click.argument("thread_id", type=int)
def remove_vote(thread_id):
    """Remove your vote from a thread."""
    api_key = load_api_key()
    res = requests.delete(f"{API_URL}/vote", headers={"apikey": api_key}, json={
        "thread_id": thread_id,
        "vote_type": "upvote"  # vote_type isn't used for deletion
    })
    click.echo(res.json())

# ✅ Get Vote Count
@click.command("get-votes")
@click.argument("thread_id", type=int)
def get_votes(thread_id):
    """Get vote count for a thread."""
    api_key = load_api_key()
    headers = {"apikey": api_key}
    res = requests.get(f"{API_URL}/thread/{thread_id}/votes", headers=headers)
    click.echo(res.json())

# ✅ Delete Comment
@click.command("delete-comment")
@click.argument("comment_id", type=int)
def delete_comment(comment_id):
    """Delete your own comment."""
    api_key = load_api_key()
    res = requests.delete(f"{API_URL}/comment/{comment_id}", headers={"apikey": api_key})
    click.echo(res.json())

# ✅ Get Full Thread Details
@click.command("thread-details")
@click.argument("thread_id", type=int)
def thread_details(thread_id):
    """Get full details for a thread."""
    api_key = load_api_key()
    headers = {"apikey": api_key}
    res = requests.get(f"{API_URL}/thread/{thread_id}", headers=headers)
    click.echo(res.json())

@click.command("user-threads")
@click.argument("username")
def user_threads(username):
    """Get all threads posted by a user (via username)."""
    api_key = load_api_key()
    user_id = get_user_id(username, api_key)
    if not user_id:
        return

    res = requests.get(f"{API_URL}/user/{user_id}/threads", headers={"apikey": api_key})
    click.echo(res.json())

# ✅ Get User Comments
@click.command("user-comments")
@click.argument("username")
def user_comments(username):
    """Get all comments posted by a user (via username)."""
    api_key = load_api_key()
    user_id = get_user_id(username, api_key)
    if not user_id:
        return

    res = requests.get(f"{API_URL}/user/{user_id}/comments", headers={"apikey": api_key})
    click.echo(res.json())

# ✅ Moderate Thread (Pin/Lock)
@click.command("moderate-thread")
@click.argument("thread_id", type=int)
@click.option("--pin", is_flag=True, help="Pin the thread")
@click.option("--unpin", is_flag=True, help="Unpin the thread")
@click.option("--lock", is_flag=True, help="Lock the thread")
@click.option("--unlock", is_flag=True, help="Unlock the thread")
def moderate_thread(thread_id, pin, unpin, lock, unlock):
    """Moderate a thread (pin, lock)."""
    api_key = load_api_key()
    data = {}

    if pin:
        data["pin"] = True
    if unpin:
        data["pin"] = False
    if lock:
        data["lock"] = True
    if unlock:
        data["lock"] = False

    if not data:
        click.echo("❌ Provide at least one moderation option: --pin/--unpin/--lock/--unlock")
        return

    res = requests.patch(f"{API_URL}/thread/{thread_id}/moderate", headers={"apikey": api_key}, json=data)
    click.echo(res.json())

# ✅ Register all commands
bbs.add_command(create_community)
bbs.add_command(list_communities)
bbs.add_command(create_thread)
bbs.add_command(get_threads_by_community)
bbs.add_command(comment)
bbs.add_command(get_comments)
bbs.add_command(vote)
bbs.add_command(remove_vote)
bbs.add_command(get_votes)
bbs.add_command(delete_comment)
bbs.add_command(thread_details)
bbs.add_command(user_threads)
bbs.add_command(user_comments)
bbs.add_command(moderate_thread)
