"""Small demo CLI for the cloud-mtool package.

This script demonstrates creating the singletons without making any network
calls. It is safe to run locally and shows how to wire `Config` and `Logger`.
"""
import argparse

from cmdb_clients import CMDB, VALI, JIRA, Config, Logger


def main() -> None:
    parser = argparse.ArgumentParser(description='cloud-mtool demo')
    parser.add_argument('--config', '-c', help='Path to JSON config file', default=None)
    parser.add_argument('--dump-config', action='store_true', help='Print current config and exit')
    parser.add_argument('--set', dest='sets', action='append', help='Set config key=value (can be passed multiple times)')
    parser.add_argument('--quiet', action='store_true', help='Reduce logging level')
    args = parser.parse_args()

    if args.config:
        try:
            Config().load_file(args.config)
            print(f'Loaded config from {args.config}')
        except Exception as exc:
            print(f'Failed to load config: {exc}')

    # apply CLI sets (key=value)
    if getattr(args, 'sets', None):
        for item in args.sets:
            if '=' not in item:
                print(f'Ignoring invalid --set value: {item} (expected key=value)')
                continue
            k, v = item.split('=', 1)
            # store as string; consumer may cast
            Config().load_dict({k: v})

    if args.dump_config:
        import json

        print(json.dumps(Config().as_dict(), indent=2))
        return

    # Configure logger
    logger = Logger()
    if args.quiet:
        logger.set_level(30)  # INFO
    log = logger.get()
    log.info('Starting cloud-mtool demo (no network calls will be made)')

    # Instantiate service singletons (they won't call network on construction)
    cmdb = CMDB(Config().get('CMDB_URL', 'https://example.com'))
    vali = VALI(Config().get('VALI_URL', 'https://example.com'))
    jira = JIRA(Config().get('JIRA_URL', 'https://example.com'))

    # Show that they are singletons
    print('CMDB instance id:', id(cmdb))
    print('VALI instance id:', id(vali))
    print('JIRA instance id:', id(jira))

    # Creating them again returns same instances
    print('CMDB same?:', cmdb is CMDB(Config().get('CMDB_URL')))
    print('VALI same?:', vali is VALI(Config().get('VALI_URL')))
    print('JIRA same?:', jira is JIRA(Config().get('JIRA_URL')))


if __name__ == '__main__':
    main()
