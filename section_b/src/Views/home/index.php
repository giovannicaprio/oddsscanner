<h1><?= htmlspecialchars($title) ?></h1>

<div class="row mb-4">
    <div class="col">
        <form method="get" id="rateForm" class="form-inline">
            <div class="input-group">
                <select name="file" class="form-select" id="rateSelect">
                    <option value="">Current Rates</option>
                    <?php foreach ($storedFiles as $file): ?>
                        <option value="<?= htmlspecialchars($file) ?>" <?= $selectedFile === $file ? 'selected' : '' ?>>
                            <?= htmlspecialchars($file) ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>
        </form>
    </div>
</div>

<div class="card">
    <div class="card-header">
        <h5 class="card-title mb-0">
            Exchange Rates - <?= htmlspecialchars($rateDate) ?>
            <small class="text-muted">(Last Update: <?= htmlspecialchars($lastUpdate) ?>)</small>
        </h5>
    </div>
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Currency</th>
                        <th>Rate</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($rates as $currency => $rate): ?>
                        <tr>
                            <td><?= htmlspecialchars($currency) ?></td>
                            <td><?= number_format($rate, 4) ?></td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const loadingIndicator = document.getElementById('loadingIndicator');
    const rateSelect = document.getElementById('rateSelect');
    const rateForm = document.getElementById('rateForm');

    rateSelect.addEventListener('change', function() {
        loadingIndicator.classList.add('active');
        rateForm.submit();
    });

    // Show loading indicator when navigating away
    window.addEventListener('beforeunload', function() {
        loadingIndicator.classList.add('active');
    });

    // Handle back/forward browser navigation
    window.addEventListener('pageshow', function(event) {
        if (event.persisted) {
            loadingIndicator.classList.remove('active');
        }
    });
});
</script> 