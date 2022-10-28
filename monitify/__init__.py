__app_name__ = "monitify"
__version__ = "0.1.0"

(
    SUCCESS,
    CONFIG_ERROR,
    IO_ERROR,
    NETWORK_ERROR
) = range(4)

ERRORS = {
    CONFIG_ERROR: "configuration error",
    IO_ERROR: "input/output error",
    NETWORK_ERROR: "network error"
}
