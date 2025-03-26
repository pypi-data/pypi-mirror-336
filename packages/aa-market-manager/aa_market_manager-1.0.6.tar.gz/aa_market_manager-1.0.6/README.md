# Market Manager for Alliance Auth

Market Manager and Market Browser plugin for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth/).

Inspired by [EveMarketer](https://evemarketer.com/), [Fuzzworks Market](https://market.fuzzwork.co.uk/browser/) and all those that came before them

![Screenshot](https://i.imgur.com/BBQ1kAM.png)

![Screenshot](https://i.imgur.com/XmY6BRp.png)
![Screenshot](https://i.imgur.com/vHLy3xP.png)

## Features

- Market Browser
  - Item Search with Autocomplete
  - Buy/Sell Orders
  - Region filtering
  - Order highlighting on Corporation and User ownership of Orders
  - Item Statistics, Medians and Percentiles
- Order Types
  - Public Orders
  - Character Orders
  - Corporation Orders
  - Private Structures Orders
- Configurable Alerts
  - Supply Alerts, Ensure adequate volume is on the market at a given price.
  - Price Alerts, Highlights orders that breach a given threshold to find Scalpers and market abuse.
  - Price Alerts (Bargains!), Flip the logic to find bargains like dreads in surrounding regions.
- Alert Destinations
  - Discord Webhooks
  - AA Discordbot channel messages

## Features - Technical

- Corporation Orders
  - A Title/Role checker, to find valid tokens to fetch orders.
- Private Structure Orders
  - Requires mapping tokens to their allowed Structures and/or Corporation's Structures.
- Structure ID Resolver
  - Resolves Stations via Django-EveUniverse EveEntity resolver
  - Resolves Citadels internally
    - Fetches Corporation Citadels from Corporation Tokens loaded with the appropriate EVE Roles ("Station_Manager")
    - get_universe_structures_structure_id requires docking ACL Access. As there is no way to tell who has docking (even the owner corporation is not a guarantee),
- Will detect and use any tokens loaded by other means, if you request the scopes as part of a wider scoped app (Such as an Audit tool etc.)
- Managed WatchConfigs, to allow external apps to manage and create their own configs.
  - Very basic currently
  - Supports Generating and maintaining WatchConfigs for a given fit.

## Planned Features

- Private Structure Orders
  - Failing to resolve will disable the token mapping to avoid error-bans.
- Configurable Alerts
  - Re-List detection, Highlight characters buying and relisting items past a configured threshold.

- Managed WatchConfigs, to allow external apps to manage and create their own configs.
  - Framework exists, need code.
  - Buybacks?!?

## Installation

### Step 1 - Django Eve Universe

Market Manager is an App for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth/), Please make sure you have this installed. Market Manager is not a standalone Django Application

Market Manager needs the App [django-eveuniverse](https://gitlab.com/ErikKalkoken/django-eveuniverse) to function. Please make sure it is installed before continuing.

### Step 2 - Install app

```shell
pip install aa-market-manager
```

### Step 3 - Configure Auth settings

Configure your Auth settings (`local.py`) as follows:

- Add `'marketmanager'` to `INSTALLED_APPS`
- Add below lines to your settings file:

```python
## Settings for AA-MarketManager
# Market Orders
CELERYBEAT_SCHEDULE['marketmanager_fetch_public_market_orders'] = {
    'task': 'marketmanager.tasks.fetch_public_market_orders',
    'schedule': crontab(minute="0", hour='*/3'),
    'apply_offset': True,
}
CELERYBEAT_SCHEDULE['marketmanager_fetch_all_character_orders'] = {
    'task': 'marketmanager.tasks.fetch_all_character_orders',
    'schedule': crontab(minute="0", hour='*/3'),
    'apply_offset': True,
}
CELERYBEAT_SCHEDULE['marketmanager_fetch_all_corporation_orders'] = {
    'task': 'marketmanager.tasks.fetch_all_corporation_orders',
    'schedule': crontab(minute="0", hour='*/3'),
    'apply_offset': True,
}
CELERYBEAT_SCHEDULE['marketmanager_fetch_all_structure_orders'] = {
    'task': 'marketmanager.tasks.fetch_all_structure_orders',
    'schedule': crontab(minute="0", hour='*/3'),
    'apply_offset': True,
}
# Structure Information
CELERYBEAT_SCHEDULE['marketmanager_fetch_public_structures'] = {
    'task': 'marketmanager.tasks.fetch_public_structures',
    'schedule': crontab(minute="0", hour="4"),
    'apply_offset': True,
}
CELERYBEAT_SCHEDULE['marketmanager_update_private_structures'] = {
    'task': 'marketmanager.tasks.update_private_structures',
    'schedule': crontab(minute="0", hour="5"),
    'apply_offset': True,
}
CELERYBEAT_SCHEDULE['marketmanager_fetch_all_corporations_structures'] = {
    'task': 'marketmanager.tasks.fetch_all_corporations_structures',
    'schedule': crontab(minute="0", hour="6"),
    'apply_offset': True,
}
# Watch Configs
CELERYBEAT_SCHEDULE['marketmanager_update_managed_supply_configs'] = {
    'task': 'marketmanager.tasks.update_managed_supply_configs',
    'schedule': crontab(minute='0', hour='2'),
}
CELERYBEAT_SCHEDULE['marketmanager_run_all_watch_configs'] = {
    'task': 'marketmanager.tasks.run_all_watch_configs',
    'schedule': crontab(minute="0", hour='*/3'),
}
# Background Tasks
CELERYBEAT_SCHEDULE['marketmanager_update_all_type_statistics'] = {
    'task': 'marketmanager.tasks.update_all_type_statistics',
    'schedule': crontab(minute='0', hour='7'),
}
# Cleanup
CELERYBEAT_SCHEDULE['marketmanager_garbage_collection'] = {
    'task': 'marketmanager.tasks.garbage_collection',
    'schedule': crontab(minute='0', hour="0"),
}
```

### Step 4 - Maintain Alliance Auth

- Run migrations `python manage.py migrate`
- Gather your staticfiles `python manage.py collectstatic`
- Restart your project `supervisorctl restart myauth:`

### Step 5 - Pre-Load Django-EveUniverse

- `python manage.py eveuniverse_load_data map` This will load Regions, Constellations and Solar Systems

### Step 6 (Optional) - Further Pre-Load Django-EveUniverse

This is less required the more you have used eveuniverse in the past

- `python manage.py eveuniverse_load_data ships --types-enabled-sections market_groups` This will load Ships, which are nearly universally on the market
- `python manage.py eveuniverse_load_data structures`, this will load Structures for use in Filters
- `python manage.py marketmanager_preload_common_eve_types` This will preload a series of Types using Groups and Categories I've analyzed to be popular on the market, please note this currently will not import MarketGroups until a market update is run for the first time, this may impact your ability to make SupplyConfigs immediately.

### Step 7 - Configuration

In the Admin interface, visit `marketmanager` or `<AUTH-URL>/admin/marketmanager`

### Public Market Configuration

Select the Regions you would like to pull Public Market Data for

- Please note Jita (The Forge) is not trivial and will take several minutes to pull and process depending on your hardware.

### TypeStatistics Calculation Configurations

Select the Regions you would like to calculate Percentiles, Medians and Weighted Averages for

- We always calculate these stats across New Eden, but these will likely match Public Market Configuration or the regions where your Private Structures are located.
- Supply Configs require The Forge selected to use The Forge(Jita) Relative Pricing.
- An item must have a minimum amount of orders to be calculated (see settings)

### Private Configs

Map the appropriate tokens with Access to Docking and Market (this cant be assumed), to the right Structures And/Or Corps.

## WatchConfig Types

Configure some supply alerts

### Supply Check

- Highlight Types (Items), that fail to meet a defined config
- Volume of Items at given price in location
Example. Warn if there is less than 1,000,000 Units of Oxygen Isotopes under 1,000 ISK/Unit, in 9KOE-A.

### Bargain Finder WIP

- Highlights Orders that meet a defined config.
Example. Notify if Naglfars under 3,000,000,000 ISK/Unit are on sale in Curse NPC Stations

### Scalp Checker WIP

- Highlights Orders, that breach Jita/Universe price.
Example. Notify Leadership that Ariel Rin is selling Nanite Repair Paste at over 500% Jita price in Staging.

### Margin Check

- Compares the lowest/highest orders in a source location to a destination.
- Either Importing a market or Exporting with Buy/Sell order choices for both source and destination
- Optionally can include a freight cost in calculations

## Managed Watch Configs

### Fittings

- Managed By App = `fittings`
- Managed App-Identifier = `fittings.fit.<FIT_ID>`
- Managed App Reason = A user facing reason
- ... a slightly limited subset of WatchConfig settings that will be replicated on each WatchConfig created.

## Permissions

| Perm | Admin Site  | Perm | Description |
| --- | --- | --- | --- |
| basic_market_browser | nill | Can access the Standard Market Browser | Can access the normal user facing market browser|
| advanced_market_browser | nill | Can access the Advanced Market Browser | Can access the more advanced management browser with private details|
| order_highlight_user | nill | Can access other character's data for own alliance. | Enables Highlighting a users own Orders in the Market Browser|
| order_highlight_corporation | nill | Can access other character's data for own corp. | Enables Highlighting the orders of a users corporation in the Market Browser|
| can_add_token_character | nill | Can add a Character Token with required scopes | Enables the "Add Character Token" button to request the needed scopes from a user|
| can_add_token_corporation | nill | Can add a Corporation Token with required scopes | Enables the "Add Corporation Token" button to request the needed scopes from a user|

## Settings

| Name | Description | Default |
| --- | --- | --- |
|`MARKETMANAGER_CLEANUP_DAYS_STRUCTURE`| Number of days without an update, before considering a Structure stale and to be deleted | 30 |
|`MARKETMANAGER_CLEANUP_DAYS_ORDER`| Number of days without an update, before considering an Order stale and to be deleted | 30|
|`MARKETMANAGER_TASK_PRIORITY_ORDERS`| Celery task priority for Order tasks | 5|
|`MARKETMANAGER_TASK_PRIORITY_STRUCTURES`| Celery task priority for Structure tasks | 4|
|`MARKETMANAGER_TASK_PRIORITY_BACKGROUND`| Celery task priority for Background tasks | 7|
|`MARKETMANAGER_TASK_PRIORITY_SUPPLY_CONFIGS`| Celery task priority for SupplyConfig tasks, This is Lower than Orders to ensure it runs while Orders are all up to date | 6|
|`MARKETMANAGER_TASK_PRIORITY_PRICE_CONFIGS`| Celery task priority for PriceConfig tasks, This is Lower than Orders to ensure it runs while Orders are all up to date | 6|
|`MARKETMANAGER_WEBHOOK_COLOUR_ERROR`| Webhook colour for Errors | 16711710|
|`MARKETMANAGER_WEBHOOK_COLOUR_WARNING`| Webhook colour for Errors | 14177041|
|`MARKETMANAGER_WEBHOOK_COLOUR_INFO`| Webhook colour for Errors  | 42751|
|`MARKETMANAGER_WEBHOOK_COLOUR_SUCCESS`| Webhook colour for Success | 6684416|
|`MARKETMANAGER_TYPESTATISTICS_MINIMUM_ORDER_COUNT` | Minimum number of Orders to exist before calculating Medians, Averages and Percentiles | 10 |

## Third Party Integrations

Creating Watch Configs from external applications is relatively straight forward and Market Manager provides an Optional Model for keeping track of these Watch Configs.

How an app maintains these Watch Configs is left to the developer, but Fittings provides a decent starting point using App Signals and referencing the Managed Watch Config model.

managed_app should follow python referencing convention. `fittings`, `projectname.modulename`
managed_app_identifier is up to the app, but i would suggest following from Fittings, `fittings.fit.{fit.id}`
managed_app_reason is presented to users as to_why_ a managed config exists, `Standard MWD Eagle x50`

```python
def marketmanager_active() -> bool:
    return apps.is_installed("marketmanager")

if marketmanager_active():
    from marketmanager.models import WatchConfig, ManagedAppConfig

    # ...
    # Maintain your Watch Configs here
    # ...
```

- Fittings (Currently from Market Manager)
  - Create and Maintain Watch Configs for x number of a Fit or Fits.

## Contributing

Make sure you have signed the [License Agreement](https://developers.eveonline.com/resource/license-agreement) by logging in at <https://developers.eveonline.com> before submitting any pull requests. All bug fixes or features must not include extra superfluous formatting changes.
