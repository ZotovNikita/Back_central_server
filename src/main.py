import sys, os
from pathlib import Path

if (dir := str(Path(os.getcwd()).parent)) not in sys.path:
    sys.path.append(dir)

import uvicorn
from src.core.settings import settings


if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        host=settings.host,
        port=settings.port,
        reload=True,
    )
