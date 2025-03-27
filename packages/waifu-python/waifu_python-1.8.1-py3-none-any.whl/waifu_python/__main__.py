import sys
import asyncio
from .cli.parser import create_parser
from .cli.commands import handle_api_command, handle_tags_command
from .API.base import APIRegistryCMD

def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.list:
        info = APIRegistryCMD.get_all_api_info()
        print("Available APIs:")
        for name, availability in info:
            
            print(f" - {name.ljust(15)} [{availability.upper()}]")
        sys.exit(0)
    
    if not args.api:
        parser.print_help()
        sys.exit(0)
    
    try:
        if args.tags:
            tags = asyncio.run(handle_tags_command(args.api))
            print(f"{args.api.capitalize()} tags: {tags}")
        else:
            nsfw = args.nsfw  
            if args.sfw:
                nsfw = False

            result = asyncio.run(handle_api_command(args.api, nsfw, args.query, args.limit))
            
            if isinstance(result, tuple):
                data, flag = result
            else:
                data = result
                flag = "nsfw" if nsfw else "sfw"
            
            print(f"\n[{flag.upper()}] Results from {args.api.capitalize()}:")
            for item in (data if isinstance(data, list) else [data]):
                print(f" - {item}")
                
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()