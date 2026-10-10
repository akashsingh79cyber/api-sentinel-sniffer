#![no_std]
#![no_main]

use aya_ebpf::{
    helpers::bpf_get_current_pid_tgid,
    macros::tracepoint,
    programs::TracePointContext,
};
use aya_log_ebpf::info;

#[tracepoint]
pub fn api_sentinel_sniffer(ctx: TracePointContext) -> u32 {
    match try_sniff(ctx) {
        Ok(ret) => ret,
        Err(ret) => ret,
    }
}

fn try_sniff(ctx: TracePointContext) -> Result<u32, u32> {
    // upper 32 bits = PID
    let pid = (bpf_get_current_pid_tgid() >> 32) as u32;
    info!(&ctx, "write() called by pid={}", pid);
    Ok(0)
}

#[cfg(not(test))]
#[panic_handler]
fn panic(_info: &core::panic::PanicInfo) -> ! {
    loop {}
}
