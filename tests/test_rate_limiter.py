import pytest

def test_limiter_api():
    from sec_edgar_downloader.rate_limiter import RateLimiter

    with RateLimiter('test-session') as limiter:
        for idx in range(0, 11):
            if idx < 10:
                assert limiter.ready() is True
                limiter.inc()

            else:
                if limiter.ready() is True:
                    import pdb; pdb.set_trace()
                    pass

                assert limiter.ready() is False

def test_delay_and_reset():
    import time

    from sec_edgar_downloader.rate_limiter import RateLimiter
    with RateLimiter('delay-and-reset') as limiter:
        for idx in range(0, 11):
            limiter.inc()

        assert limiter.ready() is False

    with RateLimiter('delay-and-reset') as limiter:
        assert limiter.ready() is False

    time.sleep(1)
    with RateLimiter('delay-and-reset') as limiter:
        assert limiter.ready() is True

def test_scope():
    from sec_edgar_downloader.rate_limiter import RateLimiter

    rl_one = RateLimiter('scope-one')
    for idx in range(0, 10):
        rl_one.inc()

    with RateLimiter('scope-two') as rl_two:
        for idx in range(0, 11):
            if idx < 10:
                assert rl_two.ready() is True
                rl_two.inc()

            else:
                assert rl_two.ready() is False

def test_block():
    from sec_edgar_downloader.rate_limiter import RateLimiter

    rl_one = RateLimiter('block-one')
    for idx in range(0, 10):
        rl_one.inc()

    with RateLimiter('block-one') as rl_two:
        for idx in range(0, 11):
            if idx < 1:
                assert rl_two.ready() is False
                rl_one.dec()
            else:
                assert rl_two.ready() is True
