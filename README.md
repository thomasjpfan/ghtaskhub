# thomasjpfan's Task Hub

Automate all the tasks!

## Install

1. Install ghtaskhub. (I recommend using [pipx](https://pipxproject.github.io/pipx/))

```python
pip install git+http://github.com/thomasjpfan/taskhub
```

2. Place your GitHub token and taskhub repo in your env:

```bash
export GITHUB_TOKEN=xxxxx
export TASKHUB_REPO=thomasjpfan/taskhub
```

## Usage

- Move completed issues and pull requests into done. Note this is run on the CI every hour.

```bash
ghtaskhub all sync
```

- Move a "Waiting for Response" card to Actionable:

```bash
ghtaskhub pytorch/pytorch actionable 44459
```

- Move a "Actionable" card  to "Waiting for Response"

```bash
ghtaskhub pytorch/pytorch response 44459
```

- Add task to bucket:

```bash
ghtaskhub pytorch/pytorch bucket 44459
```

- Create a project with the correct format

```bash
ghtaskhub pytorch/pytorch sync
```

## License

This repo is under the [MIT License](LICENSE).
