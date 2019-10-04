def test_mark_test(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.instrument('a_mark')
        def test_mark():
            assert True
    """
    )

    result = testdir.runpytest("-vs")

    result.stdout.fnmatch_lines("---> instrument mark: ('a_mark',)*")


def test_result_call_pass(testdir):
    testdir.makepyfile(
        """
        def test_passes():
            assert True
    """
    )

    result = testdir.runpytest("-vs")

    # ToDo: check duration somehow
    result.stdout.fnmatch_lines(
        "---> result: test_result_call_pass.py::test_passes, call, passed, *"
    )


def test_result_call_fails(testdir):
    testdir.makepyfile(
        """
        def test_fails():
            assert False
    """
    )

    result = testdir.runpytest("-vs")

    # ToDo: check duration somehow
    result.stdout.fnmatch_lines(
        "---> result: test_result_call_fails.py::test_fails, call, failed, *"
    )


def test_result_setup_pass(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.fixture
        def setup_passes():
            pass

        def test_passes(setup_passes):
            assert True
    """
    )

    result = testdir.runpytest("-vs")

    # ToDo: check duration somehow
    result.stdout.fnmatch_lines(
        "---> result: test_result_setup_pass.py::test_passes, setup, passed, *"
    )


def test_result_setup_fails(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.fixture
        def setup_fails():
            assert False

        def test_passes(setup_fails):
            assert True
    """
    )

    result = testdir.runpytest("-vs")

    # ToDo: check duration somehow
    result.stdout.fnmatch_lines(
        "---> result: test_result_setup_fails.py::test_passes, setup, failed, *"
    )


def test_result_teardown_pass(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.fixture
        def teardown_passes():
            yield
            pass

        def test_passes(teardown_passes):
            assert True
    """
    )

    result = testdir.runpytest("-vs")

    # ToDo: check duration somehow
    result.stdout.fnmatch_lines(
        "---> result: test_result_teardown_pass.py::test_passes, teardown, passed, *"
    )


def test_result_teardown_fails(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.fixture
        def teardown_fails():
            yield

            assert False

        def test_passes(teardown_fails):
            assert True
    """
    )

    result = testdir.runpytest("-vs")

    # ToDo: check duration somehow
    result.stdout.fnmatch_lines(
        "---> result: test_result_teardown_fails.py::test_passes, teardown, failed, *"
    )
