from core.bot import ShorekeeperBot


if __name__ == '__main__':
    try:
        bot = ShorekeeperBot.get_instance()
        bot.run_bot()
    except Exception as e:
        print(f'Bot startup failed: {e}', flush=True)
        import traceback
        traceback.print_exc()
        raise
