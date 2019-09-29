def test_mark_test(testdir):
    print(f"testdir: {testdir}")
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.instrument('a_mark')
        def test_mark():
            assert True
    """
    )

    result = testdir.runpytest("-vs")

    result.stdout.fnmatch_lines("*instrument mark: ('a_mark',)*")
