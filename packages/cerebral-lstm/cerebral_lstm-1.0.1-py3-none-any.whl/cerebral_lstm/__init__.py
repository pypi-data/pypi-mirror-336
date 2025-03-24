import torch
import torch.nn as nn

__version__ = '1.0.1'

class CerebralLSTMCell(nn.Module):
    def __init__(self, input_size, hidden_size, use_xavier=False):
        super(CerebralLSTMCell, self).__init__()
        self.hidden_size = hidden_size
        self.input_size = input_size
        self.use_xavier = use_xavier

        # Upper pathway parameters
        self.W_uf = nn.Parameter(torch.Tensor(input_size + hidden_size, hidden_size))
        self.W_ui = nn.Parameter(torch.Tensor(input_size + hidden_size, hidden_size))
        self.W_uc = nn.Parameter(torch.Tensor(input_size + hidden_size, hidden_size))
        self.W_uo = nn.Parameter(torch.Tensor(input_size + hidden_size, hidden_size))
        
        # Lower pathway parameters
        self.W_lf = nn.Parameter(torch.Tensor(input_size + hidden_size, hidden_size))
        self.W_li = nn.Parameter(torch.Tensor(input_size + hidden_size, hidden_size))
        self.W_lc = nn.Parameter(torch.Tensor(input_size + hidden_size, hidden_size))
        self.W_lo = nn.Parameter(torch.Tensor(input_size + hidden_size, hidden_size))

        # Biases
        self.b_uf = nn.Parameter(torch.zeros(hidden_size))
        self.b_ui = nn.Parameter(torch.zeros(hidden_size))
        self.b_uc = nn.Parameter(torch.zeros(hidden_size))
        self.b_uo = nn.Parameter(torch.zeros(hidden_size))
        
        self.b_lf = nn.Parameter(torch.zeros(hidden_size))
        self.b_li = nn.Parameter(torch.zeros(hidden_size))
        self.b_lc = nn.Parameter(torch.zeros(hidden_size))
        self.b_lo = nn.Parameter(torch.zeros(hidden_size))

        # Initialize weights
        self.init_weights()

    def init_weights(self):
        """Initialize weights with soft complementarity applied only to similar weights"""
        # Upper pathway initialization
        for param in [self.W_uf, self.W_ui, self.W_uo]:
            nn.init.kaiming_normal_(param, mode='fan_in', nonlinearity='sigmoid')
        nn.init.xavier_normal_(self.W_uc, gain=nn.init.calculate_gain('tanh'))
        
        # Lower pathway initialization
        for param in [self.W_lf, self.W_li, self.W_lo]:
            nn.init.kaiming_normal_(param, mode='fan_in', nonlinearity='sigmoid')
        nn.init.xavier_normal_(self.W_lc, gain=nn.init.calculate_gain('tanh'))
        
        # Apply soft complementarity only to similar weights
        self.apply_targeted_soft_complementarity(atol=1e-4)

    def apply_targeted_soft_complementarity(self, atol=1e-4):
        """Apply soft complementarity only to weights that are too similar"""
        with torch.no_grad():
            # Check and modify only the weights that are too similar
            if torch.allclose(self.W_uf, self.W_lf, atol=atol):
                self.W_lf.add_(torch.randn_like(self.W_lf) * 0.1)
            if torch.allclose(self.W_ui, self.W_li, atol=atol):
                self.W_li.add_(torch.randn_like(self.W_li) * 0.1)
            if torch.allclose(self.W_uc, self.W_lc, atol=atol):
                self.W_lc.add_(torch.randn_like(self.W_lc) * 0.1)
            if torch.allclose(self.W_uo, self.W_lo, atol=atol):
                self.W_lo.add_(torch.randn_like(self.W_lo) * 0.1)

    def forward(self, x, h_prev, cell_states):
        UC_prev, LC_prev = cell_states
        combined = torch.cat([h_prev, x], dim=1)
        
        # Upper pathway
        Uf = torch.sigmoid(combined @ self.W_uf + self.b_uf)
        Ui = torch.sigmoid(combined @ self.W_ui + self.b_ui)
        UC_tmp = torch.tanh(combined @ self.W_uc + self.b_uc)
        UC = Uf * UC_prev + Ui * UC_tmp
        Uo = torch.sigmoid(combined @ self.W_uo + self.b_uo)
        
        # Lower pathway
        Lf = torch.sigmoid(combined @ self.W_lf + self.b_lf)
        Li = torch.sigmoid(combined @ self.W_li + self.b_li)
        LC_tmp = torch.tanh(combined @ self.W_lc + self.b_lc)
        LC = Lf * LC_prev + Li * LC_tmp
        Lo = torch.sigmoid(combined @ self.W_lo + self.b_lo)
        
        h_next = Uo * torch.tanh(UC) + Lo * torch.tanh(LC)
        return h_next, (UC, LC)

    def init_hidden(self, batch_size=1):
        """Initialize hidden and cell states"""
        device = next(self.parameters()).device
        return (
            torch.zeros(batch_size, self.hidden_size, device=device),
            (
                torch.zeros(batch_size, self.hidden_size, device=device),
                torch.zeros(batch_size, self.hidden_size, device=device)
            )
        )

class CerebralLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers=1, use_xavier=False, dropout=0.0):
        super(CerebralLSTM, self).__init__()
        self.num_layers = num_layers
        self.dropout = nn.Dropout(dropout) if dropout > 0 else None
        
        self.layers = nn.ModuleList([
            CerebralLSTMCell(
                input_size=input_size if i == 0 else hidden_size,
                hidden_size=hidden_size,
                use_xavier=use_xavier
            ) for i in range(num_layers)
        ])
        
    def forward(self, x, hidden_states=None):
        """x: (seq_len, batch_size, input_size)"""
        seq_len, batch_size, _ = x.size()
        
        if hidden_states is None:
            hidden_states = [layer.init_hidden(batch_size) for layer in self.layers]
            
        outputs = []
        for t in range(seq_len):
            x_t = x[t]
            new_hidden = []
            for i, (layer, (h_prev, cells)) in enumerate(zip(self.layers, hidden_states)):
                h_next, new_cells = layer(x_t, h_prev, cells)
                x_t = h_next  # Pass output to next layer
                
                # Apply dropout between layers (except last layer)
                if self.dropout and i < self.num_layers - 1:
                    x_t = self.dropout(x_t)
                
                new_hidden.append((h_next, new_cells))
            hidden_states = new_hidden
            outputs.append(h_next)
            
        return torch.stack(outputs), hidden_states
