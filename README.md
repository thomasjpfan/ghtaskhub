# thomasjpfan's Task Hub

Automate all the tasks!

## Usage on CI

1. Move completed issues and pull requests into done. Note this is run on the CI every hour.

```python
gh workflow run -R thomasjpfan/taskhub sync
```

2. Move a "Needs Response" card to actionable:

```python
gh workflow run -R thomasjpfan/taskhub actionable -f repo=numpy/numpy -f number=12345
```

3. Create a project with the correct format

```python
gh workflow run -R thomasjpfan/taskhub create -f repo=numpy/numpy
```


## License

This repo is under the [MIT License](LICENSE).
