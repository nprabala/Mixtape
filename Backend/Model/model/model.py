import torch
import torch.nn as nn
import torch.nn.functional as F
from base import BaseModel
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

class MidiLSTM(BaseModel):
    def __init__(self, vocab_size, embed_size, hidden_size, num_layers=1, dropout=0.1):
        """
        Parameters
        ----------
        vocab_size : int
            Dimension of vocabulary
        hidden_size : int
            Dimension of the hidden layer outputs
        num_layers : int
            Number of LSTMs stacked on each other
        """
        super(MidiLSTM, self).__init__()
        self.vocab_size = vocab_size
        self.embed_size = embed_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.embed = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, num_layers=num_layers)
        self.melody_classifier = nn.Linear(hidden_size, vocab_size)
        self.chord_classifier = nn.Linear(hidden_size, vocab_size)
        self.hidden = self.init_hidden()

    def init_hidden(self):
        """
        Initialize hidden input for LSTM
            (num_layers, batch_size, hidden_size)
        """
        return (torch.zeros(self.num_layers, 1, self.hidden_size),
                torch.zeros(self.num_layers, 1, self.hidden_size))

    def forward(self, data, extra=None):
        """
        Forward pass through LSTM
        Parameters
        ----------
        x : torch.tensor (sequence_len, batch_size, vocab_size)
            input to model
        Returns
        -------
        melody_out : torch.tensor (sequence_len, batch_size, vocab_size)
            Melody softmax output (only want one note)
        chord_out : torch.tensor (sequence_len, batch_size, vocab_size)
            Chord sigmoid output (want chords)
        """
        x = data['melody_x']
        seq_lengths = extra['seq_lengths']
        embed = self.embed(x)

        # pack up sequences by length
        packed_embed = pack_padded_sequence(embed, seq_lengths)

        out, self.hidden = self.lstm(packed_embed, self.hidden)
        melody_out = F.softmax(self.melody_classifier(out))
        chord_out = F.sigmoid(self.chord_classifier(out))

        output = {
            'melody_out': melody_out,
            'chord_out': chord_out
        }

        return output



class MnistModel(BaseModel):
    def __init__(self, num_classes=10):
        super(MnistModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, num_classes)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)
