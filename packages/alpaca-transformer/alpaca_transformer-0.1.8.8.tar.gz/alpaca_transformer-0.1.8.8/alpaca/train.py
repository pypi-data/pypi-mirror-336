import torch
import torch.nn as nn
import torch.optim as optim
from tqdm.auto import tqdm
import wandb
from .validate import validate


def train(epochs, transformer, loss_fn, train_dl, optimizer=optim.Adam, lr=1e-5, device=None, validate_data=False, 
          validation_dl=None, lr_scheduler=False, wandb_tracking=None, pad_token_id=0):
    if not device:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    transformer.to(device)
    optimizer = optim.Adam(transformer.parameters(), lr=lr)
    
    # Loss function with padding token ignored
    loss_fn = nn.CrossEntropyLoss(ignore_index=pad_token_id)
    
    if wandb_tracking:
        # Initialize wandb
        wandb.init(project=wandb_tracking, config={"Learning_Rate": lr, "Epochs": epochs})
    
    for epoch in range(epochs):
        transformer.train()
        total_loss = 0
        count = 0

        # Create progress bar for batch iteration
        batch_iterator = tqdm(train_dl, desc=f'Epoch {epoch+1}/{epochs}', leave=True, 
                             bar_format='{l_bar}{bar:20}{r_bar}')
        
        prev_loss = None  # Store the previous batch's loss
        avg_loss_decrease = 0  # Track the average loss decrease

        for tensor_tokens in batch_iterator:
            tensor_tokens = tensor_tokens.to(device)

            # Forward pass
            out = transformer(tensor_tokens[:, :-1], tensor_tokens[:, :-1])

            # Targets are the same as input but shifted by one token
            target = tensor_tokens[:, 1:].to(device)

            # Calculate loss
            loss = loss_fn(out.view(-1, out.size(-1)), target.reshape(-1))

            # Backward pass
            optimizer.zero_grad()
            loss.backward()

            # Gradient clipping to avoid exploding gradients
            torch.nn.utils.clip_grad_norm_(transformer.parameters(), max_norm=1.0)

            optimizer.step()

            total_loss += loss.item()
            count += 1

            # Track the change in loss
            if prev_loss is not None:
                loss_decrease = prev_loss - loss.item()
                avg_loss_decrease = (avg_loss_decrease * (count - 1) + loss_decrease) / count  # Running average of loss decrease

            prev_loss = loss.item()

            # Update progress bar with batch loss, average loss, and loss decrease
            avg_loss = total_loss / count
            batch_iterator.set_postfix({
                "Batch Loss": f"{loss.item():.4f}",
                "Avg Loss": f"{avg_loss:.4f}",
                "Loss Decrease": f"{avg_loss_decrease:.4f}"
            })

            # Log batch loss to wandb
            if wandb_tracking:
                wandb.log({"batch_train_loss": loss.item(), "epoch": epoch}, commit=True)
        
        epoch_loss = total_loss / len(train_dl)

        # Log epoch loss to wandb
        if wandb_tracking:
            wandb.log({"epoch_train_loss": epoch_loss}, commit=True)

        print(f"Epoch: {epoch+1} | Epoch Loss: {epoch_loss:.4f}")

        if validate_data and validation_dl:
            val_loss = validate(transformer, validation_dl, loss_fn, device)
            print(f"Validation Loss: {val_loss:.4f}")
            
            # Log validation loss to wandb
            if wandb_tracking:
                wandb.log({"epoch_validation_loss": val_loss}, commit=True)

        if lr_scheduler:
            scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3, verbose=True)
            scheduler.step(epoch_loss)