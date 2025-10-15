import { test, expect } from '@playwright/test';

test.describe('Unavailable Dogs Display Enhancement', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display unavailable dogs checkbox', async ({ page }) => {
    // Check that the unavailable dogs checkbox exists
    const unavailableCheckbox = page.getByRole('checkbox', { name: /show unavailable dogs/i });
    await expect(unavailableCheckbox).toBeVisible();
    
    // Checkbox should be unchecked by default
    await expect(unavailableCheckbox).not.toBeChecked();
  });

  test('should interact with unavailable checkbox', async ({ page }) => {
    const unavailableCheckbox = page.getByRole('checkbox', { name: /show unavailable dogs/i });
    
    // Click the unavailable checkbox
    await unavailableCheckbox.check();
    await expect(unavailableCheckbox).toBeChecked();
    
    // Uncheck it
    await unavailableCheckbox.uncheck();
    await expect(unavailableCheckbox).not.toBeChecked();
  });

  test('should display status badges on dog tiles', async ({ page }) => {
    // Wait for dog tiles to load
    await page.waitForSelector('[data-testid="dog-tile"]', { timeout: 10000 });
    
    // Check that status badges are visible
    const statusBadges = page.locator('[data-testid="status-badge"]');
    const badgeCount = await statusBadges.count();
    
    // Should have at least one status badge
    expect(badgeCount).toBeGreaterThan(0);
    
    // Check that badges have valid status text
    const firstBadge = statusBadges.first();
    const badgeText = await firstBadge.textContent();
    expect(['Available', 'Pending', 'Adopted']).toContain(badgeText);
  });

  test('should persist unavailable checkbox state in localStorage', async ({ page }) => {
    const unavailableCheckbox = page.getByRole('checkbox', { name: /show unavailable dogs/i });
    
    // Check the unavailable checkbox
    await unavailableCheckbox.check();
    
    // Refresh the page
    await page.reload();
    
    // Checkbox should still be checked after refresh
    await expect(unavailableCheckbox).toBeChecked();
  });

  test('should show context-aware empty state messages', async ({ page }) => {
    // This test may need to be adapted based on actual data
    // For now, just check that the empty state container exists
    const availableCheckbox = page.getByRole('checkbox', { name: /show available dogs/i });
    const unavailableCheckbox = page.getByRole('checkbox', { name: /show unavailable dogs/i });
    
    // Uncheck both checkboxes to trigger empty state
    await availableCheckbox.uncheck();
    await unavailableCheckbox.uncheck();
    
    // Should show some kind of empty state message
    // This selector may need adjustment based on actual implementation
    await expect(page.getByText(/no dogs/i)).toBeVisible();
  });
});