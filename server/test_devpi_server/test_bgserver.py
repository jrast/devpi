import sys
import random
import py
import pytest
from devpi_server.main import main


@pytest.mark.skipif("not config.option.slow")
def test_server_commands(tmpdir, monkeypatch):
    monkeypatch.setenv("DEVPI_SERVERDIR", tmpdir)
    monkeypatch.setattr(sys, "argv",
                        [str(py.path.local.sysfind("devpi-server"))])
    if sys.platform == "win32":
        # Windows strips the "exe" from the first argument of sys.argv
        # The first entry in sys.path contains the executable path
        monkeypatch.setattr(sys, "path",
                            [sys.argv[0]] + sys.path)
        monkeypatch.setattr(sys, "argv",
                            [sys.argv[0][:-4]])


    portopt = "--port=" + str(random.randint(2001, 64000))
    main(["devpi-server", "--start", portopt])
    try:
        main(["devpi-server", "--status"])
        main(["devpi-server", "--log"])
        # make sure we can't start a server if one is already running
        with pytest.raises(SystemExit):
            main(["devpi-server", "--start", portopt])
    finally:
        main(["devpi-server", "--stop"])
