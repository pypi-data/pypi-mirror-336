import typer

from omnilearned.train import run as run_training
from omnilearned.dataloader import load_data

app = typer.Typer(
    help="OmniLearned: A unified deep learning approach for particle physics"
)


@app.command()
def train(
    # General Options
    outdir: str = typer.Option(
        "", "--output_dir", "-o", help="Directory to output best model"
    ),
    save_tag: str = typer.Option("", help="Extra tag for checkpoint model"),
    dataset: str = typer.Option("top", help="Dataset to load"),
    path: str = typer.Option(
        "/pscratch/sd/v/vmikuni/PET/datasets", help="Dataset path"
    ),
    # Model Options
    use_pid: bool = typer.Option(False, help="Use particle ID for training"),
    use_add: bool = typer.Option(
        False, help="Use additional features beyond kinematic information"
    ),
    use_clip: bool = typer.Option(False, help="Use CLIP loss during training"),
    num_classes: int = typer.Option(
        2, help="Number of classes in the classification task"
    ),
    mode: str = typer.Option(
        "classifier", help="Task to run: classifier, generator, pretrain"
    ),
    # Training options
    batch: int = typer.Option(64, help="Batch size"),
    iterations: int = typer.Option(-1, help="Number of iterations per pass"),
    epoch: int = typer.Option(15, help="Number of epochs"),
    # Optimizer
    b1: float = typer.Option(0.95, help="Lion b1"),
    b2: float = typer.Option(0.98, help="Lion b2"),
    lr: float = typer.Option(5e-4, help="Learning rate"),
    wd: float = typer.Option(0.3, help="Weight decay"),
    # Model
    num_transf: int = typer.Option(6, help="Number of transformer blocks"),
    num_tokens: int = typer.Option(4, help="Number of trainable tokens"),
    num_head: int = typer.Option(8, help="Number of transformer heads"),
    K: int = typer.Option(15, help="Number of nearest neighbors"),
    radius: int = typer.Option(0.4, help="Local neighborhood radius"),
    base_dim: int = typer.Option(64, help="Base value for dimensions"),
    mlp_ratio: int = typer.Option(2, help="Multiplier for MLP layers"),
    attn_drop: float = typer.Option(0.1, help="Dropout for attention layers"),
    mlp_drop: float = typer.Option(0.1, help="Dropout for mlp layers"),
    feature_drop: float = typer.Option(0.0, help="Dropout for input features"),
):
    run_training(
        outdir,
        save_tag,
        dataset,
        path,
        use_pid,
        use_add,
        use_clip,
        num_classes,
        mode,
        batch,
        iterations,
        epoch,
        b1,
        b2,
        lr,
        wd,
        num_transf,
        num_tokens,
        num_head,
        K,
        radius,
        base_dim,
        mlp_ratio,
        attn_drop,
        mlp_drop,
        feature_drop,
    )


@app.command()
def dataloader(
    dataset: str = typer.Option(
        "top", "--dataset", "-d", help="Dataset name to download"
    ),
    folder: str = typer.Option(
        "./", "--folder", "-f", help="Folder to save the dataset"
    ),
):

    for tag in ["train", "test", "val"]:
        load_data(dataset, folder, dataset_type=tag, distributed=False)

if __name__ == "__main__":
    app()