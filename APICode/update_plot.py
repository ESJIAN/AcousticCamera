def update_plot():
    if is_recording:
        data = stream.read(CHUNK)
        frames = np.frombuffer(data, dtype=np.int16).reshape(-1, CHANNELS)

        # 添加波形电压值门槛
        if np.max(np.abs(frames)) > 4000:
            intensity_map, theta_range, phi_range = calculate_delay_and_sum(frames)

            ax1.clear()
            ax1.plot(frames)
            ax1.set_title("Waveform")

            ax2.clear()
            theta_deg = theta_range * 180 / np.pi
            phi_deg = phi_range * 180 / np.pi
            im = ax2.imshow(intensity_map, extent=[phi_deg.min(), phi_deg.max(), theta_deg.min(), theta_deg.max()], aspect='auto', origin='lower')
            # fig.colorbar(im, ax=ax2)
            ax2.set_title("Sound Intensity Distribution")
            ax2.set_xlabel("Phi (degrees)")
            ax2.set_ylabel("Theta (degrees)")

            canvas.draw()

    root.after(100, update_plot)