import torch
import torch.nn.functional as F
from data_loader.dataset import MidiDataset

def midi_loss(output, target, extra=None):
    melody_out = output['melody_out']
    chord_out = output['chord_out']
    melody_y = target['melody_y']
    chord_y = target['chord_y']

    batch_size = melody_out.size(0)
    seq_lengths = extra['seq_lengths']
    device = melody_out.device

    if MidiDataset.USE_SEQUENCE:
        flat_melody_out = melody_out
        flat_chord_out = chord_out
        flat_melody_y = melody_y
        flat_chord_y = chord_y
    else:
        # flatten (batchsize, seq_len, vocab_size) -> (batchsize * seq_len, vocab_size)
        # contiguous returns tensor with same data
        flat_melody_out = torch.tensor([]).to(device)
        flat_chord_out = torch.tensor([]).to(device)
        flat_melody_y = torch.tensor([]).long().to(device)
        flat_chord_y = torch.tensor([]).to(device)
        for i in range(batch_size):
            flat_melody_out = torch.cat((flat_melody_out, melody_out[i, :seq_lengths[i]]))
            flat_chord_out = torch.cat((flat_chord_out, chord_out[i, :seq_lengths[i]]))
            flat_melody_y = torch.cat((flat_melody_y, melody_y[i, :seq_lengths[i]].long()))
            flat_chord_y = torch.cat((flat_chord_y, chord_y[i, :seq_lengths[i]].float()))

    # melody_out = melody_out[:, seq_len-1].contiguous().view(-1, vocab_size)
    # chord_out = chord_out[:, seq_len-1].contiguous().view(-1, vocab_size)
    # melody_y = melody_y[:, seq_len-1].flatten()
    # chord_y = chord_y[:, seq_len-1].view(-1, vocab_size)

    return F.nll_loss(flat_melody_out, flat_melody_y) + F.multilabel_soft_margin_loss(flat_chord_out, flat_chord_y)

def midi_loss_chord_only(output, target, extra=None):
    melody_out = output['melody_out']
    chord_out = output['chord_out']
    melody_y = target['melody_y']
    chord_y = target['chord_y']

    batch_size = melody_out.size(0)
    seq_lengths = extra['seq_lengths']
    device = melody_out.device

    if MidiDataset.USE_SEQUENCE:
        flat_melody_out = melody_out
        flat_chord_out = chord_out
        flat_melody_y = melody_y
        flat_chord_y = chord_y
    else:
        # flatten (batchsize, seq_len, vocab_size) -> (batchsize * seq_len, vocab_size)
        # contiguous returns tensor with same data
        flat_chord_out = torch.tensor([]).to(device)
        flat_chord_y = torch.tensor([]).to(device)
        for i in range(batch_size):
            flat_chord_out = torch.cat((flat_chord_out, chord_out[i, :seq_lengths[i]]))
            flat_chord_y = torch.cat((flat_chord_y, chord_y[i, :seq_lengths[i]].float()))

    # melody_out = melody_out[:, seq_len-1].contiguous().view(-1, vocab_size)
    # chord_out = chord_out[:, seq_len-1].contiguous().view(-1, vocab_size)
    # melody_y = melody_y[:, seq_len-1].flatten()
    # chord_y = chord_y[:, seq_len-1].view(-1, vocab_size)


    return F.multilabel_soft_margin_loss(flat_chord_out, flat_chord_y)
