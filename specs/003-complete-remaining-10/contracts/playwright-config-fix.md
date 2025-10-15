# Test Infrastructure Contract: Playwright Configuration Fix

**Contract Type**: Configuration Enhancement  
**Target**: `client/playwright.config.ts`  
**Scope**: Windows compatibility for E2E test execution

## Contract Requirements

### Input Contract (Current State - BROKEN)
```typescript
// Current configuration causing Windows failures
export default defineConfig({
  // ... existing config ...
  webServer: {
    command: 'cd .. && ./scripts/start-app.sh',  // ❌ FAILS on Windows
    url: 'http://localhost:4321',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
```

**Problem**: Bash script `start-app.sh` not executable in Windows Git Bash environment

### Output Contract (Required Fix)
```typescript
// REQUIRED: Cross-platform compatible configuration
export default defineConfig({
  // ... existing config unchanged ...
  webServer: {
    command: 'npm run dev',                    // ✅ Cross-platform npm command
    url: 'http://localhost:4321',             // ✅ Keep existing URL
    reuseExistingServer: !process.env.CI,    // ✅ Keep existing reuse logic  
    timeout: 120 * 1000,                     // ✅ Keep existing timeout
  },
});
```

### Server Startup Contract
```bash
# Command behavior must remain identical
npm run dev  # Must start Astro dev server on port 4321
# Equivalent to: astro dev
# Must serve frontend with API proxy to backend on port 5100
```

### Test Execution Contract
```bash
# Must enable successful E2E test execution
npx playwright test e2e-tests/unavailable-dogs.spec.ts  # Must work after fix
npx playwright test                                     # Must work for all tests
```

## Integration Requirements

### Backend Server Contract ✅ COMPLETE
```bash
# Backend must be running independently
cd server && python app.py  # Running on http://localhost:5100
# Status: Already working, no changes required
```

### Frontend Server Contract (Fix Required)
```bash
# Frontend server startup via npm
cd client && npm run dev     # Must start on http://localhost:4321
# Must include API proxy middleware to backend
# Must serve all existing routes and static assets
```

### Test Environment Contract
```typescript
// Test execution environment requirements
baseURL: 'http://localhost:4321'    // Must connect to frontend server
// Server must be ready before tests begin
// All existing E2E tests must continue to work
```

## Error Resolution Contract

### Current Error (to be fixed)
```bash
Error: Process from config.webServer was not able to start. Exit code: 1
[WebServer] '.' is not recognized as an internal or external command
```

### Expected Behavior (after fix)
```bash
# Successful server startup
[WebServer] > dog-shelter@0.0.1 dev
[WebServer] > astro dev
[WebServer] astro v5.4.3 ready in XXXXms
[WebServer] ┃ Local    http://localhost:4321/
```

## Compatibility Contract

### Platform Support
- ✅ **Windows**: Must work in Git Bash, PowerShell, Command Prompt
- ✅ **Linux**: Must continue working in bash/zsh
- ✅ **macOS**: Must continue working in bash/zsh  

### Development Environment
- ✅ **VS Code**: Must work with integrated terminal
- ✅ **Command Line**: Must work from any shell
- ✅ **CI/CD**: Must work in GitHub Actions (existing logic preserved)

## Validation Contract

### Manual Validation
```bash
# Must execute successfully after fix
cd /c/Users/utpal/test-repo/client
npx playwright test e2e-tests/unavailable-dogs.spec.ts
```

### Automated Validation  
```typescript
// E2E tests must pass
test('unavailable dogs checkbox appears') // Must pass
test('status badges display correctly')   // Must pass  
test('localStorage persistence works')    // Must pass
test('filter combinations work')          // Must pass
```

## Backward Compatibility Contract

### No Breaking Changes Required
- ✅ All existing E2E tests must continue to pass
- ✅ Frontend server behavior unchanged
- ✅ API proxy functionality preserved
- ✅ Development workflow unchanged

### Configuration Changes Only
- ✅ Single line change: `command: 'npm run dev'`
- ✅ No dependency modifications
- ✅ No test file changes
- ✅ No server configuration changes

## Acceptance Criteria
1. ✅ Playwright tests execute successfully on Windows
2. ✅ No "command not found" errors during test startup
3. ✅ All existing E2E tests continue to pass
4. ✅ Frontend server starts correctly via npm command
5. ✅ API proxy middleware continues to function
6. ✅ Cross-platform compatibility maintained
7. ✅ No changes to test scenarios or expectations

**Implementation Size**: 1 line configuration change
**Risk Level**: Minimal (configuration-only change)  
**Dependencies**: None (npm commands already available)