import argparse
from pprint import pprint
from config import api_url
from api import Api
from output import Output, DataOutput
from special import _HelpAction

if __name__ == '__main__':
    # build our parser
    parser = argparse.ArgumentParser(add_help=False)

    # main options
    # these are always available
    parser.add_argument('-h', '--help', action=_HelpAction, help='help for help if you need some help')  # add custom help

    # the get command options
    # these are avialbe to the write command
    subparsers = parser.add_subparsers(help='commands', dest='command')
    get_parser = subparsers.add_parser('get', help='read data from blog')
    get_parser.add_argument('-u', "--users", help="Get a user or all users", action='store_true')
    get_parser.add_argument('-U', "--user", help="Get a user or all users", type=int)

    get_parser.add_argument('-p', "--posts", help="Get all blog posts", action='store_true')
    get_parser.add_argument('-P', "--post", help="Get a blog post by id", type=int)
    get_parser.add_argument('-f', "--format", choices=['html', 'json', 'response'], default='json')
    get_parser.add_argument('-s', "--spacing", type=int, default=12)

    # the get command options
    # these are available to the write command
    write_parser = subparsers.add_parser('write', help='add a post to the blog')
    write_parser.add_argument('-t', '--title', type=str, help='Post Title')
    write_parser.add_argument('-b', '--body', type=str, help='Post Body')
    write_parser.add_argument('-a', '--author', type=str, help='Author ID')
    write_parser.add_argument('-i', "--interactive", action="store_true")

    # get input from our parser
    args = parser.parse_args()

    api = Api(api_url)

    if args.command == 'get':
        spacing = args.spacing
        if args.users:
            users = Api(api_url).get_users(args.format)
            columns = ['id', 'name', 'email']
            out = DataOutput(users, args.format, columns, spacing)
            out.output()

        elif args.user:
            user = Api(api_url).get_user(args.user, args.format)
            columns = ['id', 'name', 'email']
            out = DataOutput(user, args.format, columns, spacing)
            out.output()

        elif args.posts:
            columns = ['id', 'title', 'body', 'author_id']
            posts = Api(api_url).get_posts(args.format)
            out = DataOutput(posts, args.format, columns, spacing)
            out.add_trimmer('title', spacing - 2)
            out.add_trimmer('body', spacing - 2)
            out.output()

        elif args.post:
            columns = ['id', 'title', 'body', 'author_id']
            post = Api(api_url).get_post(args.post, args.format)
            out = DataOutput(post, args.format, columns, 15)
            out.add_trimmer('title', spacing - 2)
            out.add_trimmer('body', spacing - 2)
            out.output()

    if args.command == 'write':
        if args.interactive:
            title = input('Give your post a title: ')
            body = input('What do you want to say: ')
            while True:
                authors = api.get_users()
                available_authors = "".join(["{}) {}\n".format(author['id'], author['name']) for author in authors])
                choice = input('Enter an author id: \n' + available_authors + "Choice: ")
                author_ids = [author['id'] for author in authors]
                if choice in author_ids:
                    author_id = choice
                    break
            feedback = Api(api_url).create_post(title, body, author_id)
            print(feedback['message'])
        else:
            title = args.title
            body = args.body
            author_id = args.author
            feedback = Api(api_url).create_post(title, body, author_id)
            print(feedback['message'])
