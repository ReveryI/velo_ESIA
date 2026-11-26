"""Point d'entrée CLI : construction du parser, routage et gestion des erreurs."""

from __future__ import annotations

import argparse
import logging
from collections.abc import Sequence
from pathlib import Path

from velo import __version__
from velo.commands import (
    alerts_cmd,
    collect_cmd,
    dashboard_cmd,
    favorites_cmd,
    history_cmd,
    init_cmd,
    query_cmd,
    refresh_cmd,
    station_cmd,
    status_cmd,
)
from velo.config import load_config
from velo.errors import VeloError
from velo.logging_utils import setup_logging

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_INTERRUPTED = 130

COMMAND_MODULES = (
    init_cmd,
    refresh_cmd,
    status_cmd,
    station_cmd,
    favorites_cmd,
    alerts_cmd,
    dashboard_cmd,
    collect_cmd,
    history_cmd,
    query_cmd,
)

log = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Construit le parser principal et enregistre toutes les sous-commandes.

    Returns:
        Le parser argparse complet de l'outil.
    """
    parser = argparse.ArgumentParser(
        prog="velo",
        description="Vélo - données ouvertes des vélos en libre-service (V'Lille par défaut).",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="chemin d'un config.yaml alternatif",
    )
    subparsers = parser.add_subparsers(dest="command", required=True, metavar="COMMANDE")
    for module in COMMAND_MODULES:
        module.register(subparsers)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Analyse les arguments, exécute la commande et traduit les erreurs en code de sortie.

    Args:
        argv: Arguments de la ligne de commande (``sys.argv[1:]`` si None).

    Returns:
        0 en cas de succès, 1 pour une erreur gérée, 130 après Ctrl+C.
    """
    args = build_parser().parse_args(argv)
    setup_logging() 
    try:
        config = load_config(args.config) if getattr(args, "needs_config", True) else None
        if config is not None:
            setup_logging(config.logging.level)
        return int(args.func(args, config) or EXIT_OK)
    except VeloError as exc:
        log.error("Erreur : %s", exc)  # affiché sur la console ET écrit dans le fichier de log
        return EXIT_ERROR
    except KeyboardInterrupt:
        log.info("Interrompu par l'utilisateur.")
        return EXIT_INTERRUPTED
    except Exception: 
        log.exception("Erreur inattendue")  #trace dans le fichier de log seulement
        return EXIT_ERROR


if __name__ == "__main__":
    raise SystemExit(main())